# Multimodal Digital Piano Tutoring System 🎹🤖

This repository contains the source code for the pedagogical state machine and the multimodal fusion engine, which integrates MIDI data and computer vision for real-time piano tutoring and posture analysis.

## ⚙️ Prerequisites

Before running the system, ensure you have the following installed:

* **Python:** Version 3.8 or higher.
* **Hardware:**
    * A standard RGB Webcam.
    * A Digital Piano with MIDI output.
    * A MIDI-to-USB interface cable connected to your computer.

## 📦 Dependencies

The system relies on several Python libraries. You can install all required dependencies using `pip`:

```bash
pip install opencv-python mediapipe mido python-rtmidi
```

> **Note:** `python-rtmidi` is required as a backend for the `mido` library to correctly interface with hardware MIDI ports.

## 📂 Required Assets

For the computer vision module to work, you **must** download the MediaPipe Hand Landmarker model:

1. Download the `hand_landmarker.task` file from the official Google MediaPipe documentation.
2. Place the `hand_landmarker.task` file directly in the root directory of this project (in the same folder as `hand_test.py`).

## 🚀 How to Run the System

1. Connect your digital piano to your computer via the MIDI cable.
2. Turn on the digital piano.
3. Open your terminal, navigate to the project folder, and execute the main script:

   ```bash
   python hand_test.py
   ```

4. The system will automatically detect the first available MIDI port and open your webcam. The Dynamic HUD will appear on your screen.

## 🎮 Controls & Interface

Once the HUD is running, use your computer keyboard to interact with the Curriculum Engine:

* **`1` – `6`:** Select a specific lesson or song from the pedagogical curriculum (e.g., press `6` for *Ode to Joy*).
* **`x`:** Cancel the current active lesson and return to the main menu.
* **`q`:** Safely quit the application and close all camera/MIDI ports.

## 🧠 File Structure Overview

* `hand_test.py` — The main execution script containing the video capture loop, MediaPipe kinematics engine, MIDI callback handler, and OpenCV HUD renderer.
* `curriculum.py` — The data structure housing the target sequences for the pedagogical state machine.
* `hand_landmarker.task` — The pre-trained machine learning model required by Google MediaPipe for real-time hand tracking and kinematic estimation.
