import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import mido
import math
from curriculum import CURRICULUM

# --- 1. CONFIGURATION ---
MODEL_PATH = 'hand_landmarker.task'
MIN_DETECTION_CONFIDENCE = 0.7
NUM_HANDS = 2 

TWIST_THRESHOLD_DEGREES = 40  
DROP_THRESHOLD_DEGREES = 40   

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),      
    (0, 5), (5, 6), (6, 7), (7, 8),      
    (0, 9), (9, 10), (10, 11), (11, 12), 
    (0, 13), (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20),
    (5, 9), (9, 13), (13, 17), (0, 17)   
]

playing_notes = set()

active_exercise = None
exercise_mode = False
current_seq_index = 0
current_step_hits = set()

feedback_text = "Select a lesson to begin."
feedback_color = (255, 255, 255)
feedback_time = 0

def get_note_name(midi_number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_number // 12) - 1
    return f"{notes[midi_number % 12]}{octave}"

def midi_callback(msg):
    global playing_notes, exercise_mode, current_seq_index, current_step_hits, active_exercise
    global feedback_text, feedback_color, feedback_time
    
    note_name = get_note_name(msg.note)

    if msg.type == 'note_on' and msg.velocity > 0:
        playing_notes.add(note_name)
        
        if exercise_mode and active_exercise:
            expected_notes = active_exercise["seq"][current_seq_index]
            
            if note_name in expected_notes:
                current_step_hits.add(note_name)
                
                if len(current_step_hits) == len(expected_notes):
                    current_seq_index += 1
                    current_step_hits.clear()
                    
                    if current_seq_index >= len(active_exercise["seq"]):
                        feedback_text = f"BRAVO! '{active_exercise['name']}' COMPLETED!"
                        feedback_color = (255, 255, 0)
                        feedback_time = time.time()
                        exercise_mode = False
                    else:
                        feedback_text = "GOOD!"
                        feedback_color = (0, 255, 0)
                        feedback_time = time.time()
            else:
                feedback_text = f"MISTAKE! Not {note_name}. Try again!"
                feedback_color = (0, 0, 255)
                feedback_time = time.time()
                current_step_hits.clear() 

    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
        playing_notes.discard(note_name) 

# --- 2. BAŞLATMA ---
available_ports = mido.get_input_names()
if len(available_ports) > 0:
    MIDI_PORT_NAME = available_ports[0] 
    print(f"Bağlanılan Cihaz: {MIDI_PORT_NAME}")
else:
    print("HATA: MIDI Kablosu bulunamadı!")
    exit()

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options, running_mode=vision.RunningMode.VIDEO, 
    num_hands=NUM_HANDS, min_hand_detection_confidence=MIN_DETECTION_CONFIDENCE)

# --- 3. ANA DÖNGÜ ---
def main():
    global exercise_mode, current_seq_index, current_step_hits, active_exercise
    global feedback_text, feedback_time, feedback_color
    
    try:
        inport = mido.open_input(MIDI_PORT_NAME, callback=midi_callback)
    except Exception as e:
        print(f"MIDI Hatası: {e}")
        return

    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    
    with vision.HandLandmarker.create_from_options(options) as landmarker:
        while cap.isOpened():
            success, frame = cap.read()
            if not success: continue

            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            detection_result = landmarker.detect_for_video(mp_image, int(time.time() * 1000))

            warning_message = ""

            if detection_result.hand_landmarks:
                for landmarks in detection_result.hand_landmarks:
                    pixel_coords = {}
                    for idx, landmark in enumerate(landmarks):
                        px, py = int(landmark.x * w), int(landmark.y * h)
                        pixel_coords[idx] = (px, py)
                        cv2.circle(frame, (px, py), 4, (0, 255, 0), -1)

                    for connection in HAND_CONNECTIONS:
                        start_idx, end_idx = connection
                        if start_idx in pixel_coords and end_idx in pixel_coords:
                            cv2.line(frame, pixel_coords[start_idx], pixel_coords[end_idx], (255, 255, 255), 2)

                    twist_angle, drop_angle = 0, 0
                    if 5 in pixel_coords and 17 in pixel_coords:
                        x5, y5 = pixel_coords[5]   
                        x17, y17 = pixel_coords[17] 
                        twist_angle = abs(math.degrees(math.atan((y17 - y5) / ((x17 - x5) + 0.0001))))

                    if 0 in pixel_coords and 9 in pixel_coords:
                        wx, wy = pixel_coords[0]
                        kx, ky = pixel_coords[9]
                        drop_angle = math.degrees(math.atan((wy - ky) / (abs(kx - wx) + 0.0001)))

                    if twist_angle > TWIST_THRESHOLD_DEGREES:
                        warning_message = f"WARNING: EXCESSIVE TWIST! ({int(twist_angle)} deg)"
                    elif drop_angle > DROP_THRESHOLD_DEGREES and wy > ky:
                        warning_message = f"WARNING: WRIST COLLAPSED! ({int(drop_angle)} deg)"

            # --- YENİ DİNAMİK ARAYÜZ (GUI) ---
            
            # 1. HEDEF NOTALAR (SOL ÜST KÖŞE)
            if exercise_mode:
                target_notes = active_exercise["seq"][current_seq_index]
                target_str = " & ".join(target_notes)
                progress_str = f"({current_seq_index + 1}/{len(active_exercise['seq'])})"
                
                cv2.putText(frame, f"TARGET {progress_str}: {target_str}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)
                cv2.putText(frame, f"Lesson: {active_exercise['name']} (Press 'x' to exit)", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

            # 2. O AN ÇALINAN NOTALAR (SOL TARAFA HİZALI)
            if playing_notes:
                notes_str = " - ".join(sorted(playing_notes))
                # Egzersiz modundaysa Target'ın altına in, değilse en üste çık
                y_pos_playing = 140 if exercise_mode else 50
                cv2.putText(frame, f"PLAYING: {notes_str}", (50, y_pos_playing), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # 3. BİYOMEKANİK UYARILAR (DİĞER YAZILARIN ALTINA)
            if warning_message:
                y_pos_warning = 190 if exercise_mode else 100
                cv2.putText(frame, warning_message, (50, y_pos_warning), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # 4. ANA MENÜ (SAĞ ÜST KÖŞE - SADECE DERS YOKKEN GÖZÜKÜR)
            if not exercise_mode:
                cv2.putText(frame, "=== LESSON MENU ===", (w - 350, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                y_offset = 80
                for key, val in CURRICULUM.items():
                    cv2.putText(frame, f"Press {key}: {val['name']}", (w - 400, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 255, 200), 2)
                    y_offset += 30

            # 5. GERİ BİLDİRİM "GOOD / MISTAKE" (EKRANIN TAM ORTASI)
            if time.time() - feedback_time < 2.0:
                cv2.putText(frame, feedback_text, (w//2 - 250, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, feedback_color, 3)

            cv2.imshow('AI Piano Tutor - Clean HUD Edition', frame)
            
            # --- KLAVYE KONTROLLERİ ---
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): 
                break
            elif key == ord('x') and exercise_mode:
                exercise_mode = False
                feedback_text = "Lesson Cancelled."
                feedback_color = (150, 150, 150)
                feedback_time = time.time()
            elif not exercise_mode:
                key_char = chr(key)
                if key_char in CURRICULUM:
                    active_exercise = CURRICULUM[key_char]
                    exercise_mode = True
                    current_seq_index = 0
                    current_step_hits.clear()
                    feedback_text = f"STARTING: {active_exercise['name']}"
                    feedback_color = (0, 255, 255)
                    feedback_time = time.time()

    inport.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()