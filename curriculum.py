# curriculum.py

CURRICULUM = {
    "1": {
        "name": "C Major Scale",
        "seq": [
            ("C3", "C4"), ("D3", "D4"), ("E3", "E4"), ("F3", "F4"), ("G3", "G4"), ("A3", "A4"), ("B3", "B4"), 
            ("C4", "C5"), ("D4", "D5"), ("E4", "E5"), ("F4", "F5"), ("G4", "G5"), ("A4", "A5"), ("B4", "B5"), ("C5", "C6"),
            ("B4", "B5"), ("A4", "A5"), ("G4", "G5"), ("F4", "F5"), ("E4", "E5"), ("D4", "D5"), ("C4", "C5"), 
            ("B3", "B4"), ("A3", "A4"), ("G3", "G4"), ("F3", "F4"), ("E3", "E4"), ("D3", "D4"), ("C3", "C4")
        ]
    },
    "2": {
        "name": "G Major Scale",
        "seq": [
            ("G2", "G3"), ("A2", "A3"), ("B2", "B3"), ("C3", "C4"), ("D3", "D4"), ("E3", "E4"), ("F#3", "F#4"), 
            ("G3", "G4"), ("A3", "A4"), ("B3", "B4"), ("C4", "C5"), ("D4", "D5"), ("E4", "E5"), ("F#4", "F#5"), ("G4", "G5"),
            ("F#4", "F#5"), ("E4", "E5"), ("D4", "D5"), ("C4", "C5"), ("B3", "B4"), ("A3", "A4"), ("G3", "G4"), 
            ("F#3", "F#4"), ("E3", "E4"), ("D3", "D4"), ("C3", "C4"), ("B2", "B3"), ("A2", "A3"), ("G2", "G3")
        ]
    },
    "3": {
        "name": "F Major Scale",
        "seq": [
            ("F2", "F3"), ("G2", "G3"), ("A2", "A3"), ("A#2", "A#3"), ("C3", "C4"), ("D3", "D4"), ("E3", "E4"), 
            ("F3", "F4"), ("G3", "G4"), ("A3", "A4"), ("A#3", "A#4"), ("C4", "C5"), ("D4", "D5"), ("E4", "E5"), ("F4", "F5"),
            ("E4", "E5"), ("D4", "D5"), ("C4", "C5"), ("A#3", "A#4"), ("A3", "A4"), ("G3", "G4"), ("F3", "F4"), 
            ("E3", "E4"), ("D3", "D4"), ("C3", "C4"), ("A#2", "A#3"), ("A2", "A3"), ("G2", "G3"), ("F2", "F3")
        ]
    },
    "4": {
        "name": "A Natural Minor",
        "seq": [
            ("A2", "A3"), ("B2", "B3"), ("C3", "C4"), ("D3", "D4"), ("E3", "E4"), ("F3", "F4"), ("G3", "G4"), 
            ("A3", "A4"), ("B3", "B4"), ("C4", "C5"), ("D4", "D5"), ("E4", "E5"), ("F4", "F5"), ("G4", "G5"), ("A4", "A5"),
            ("G4", "G5"), ("F4", "F5"), ("E4", "E5"), ("D4", "D5"), ("C4", "C5"), ("B3", "B4"), ("A3", "A4"), 
            ("G3", "G4"), ("F3", "F4"), ("E3", "E4"), ("D3", "D4"), ("C3", "C4"), ("B2", "B3"), ("A2", "A3")
        ]
    },
    "5": {
        "name": "D Harmonic Minor",
        "seq": [
            ("D3", "D4"), ("E3", "E4"), ("F3", "F4"), ("G3", "G4"), ("A3", "A4"), ("A#3", "A#4"), ("C#4", "C#5"), 
            ("D4", "D5"), ("E4", "E5"), ("F4", "F5"), ("G4", "G5"), ("A4", "A5"), ("A#4", "A#5"), ("C#5", "C#6"), ("D5", "D6"),
            ("C#5", "C#6"), ("A#4", "A#5"), ("A4", "A5"), ("G4", "G5"), ("F4", "F5"), ("E4", "E5"), ("D4", "D5"), 
            ("C#4", "C#5"), ("A#3", "A#4"), ("A3", "A4"), ("G3", "G4"), ("F3", "F4"), ("E3", "E4"), ("D3", "D4")
        ]
    },
    "6": {
        "name": "Song: Ode to Joy",
        "seq": [
            # THEME A (First 4 Measures)
            ("C3", "E3", "G3", "E4"),  # Left hand C Major Chord + Right hand E4
            ("E4",),                   # Hold Left hand chord, Right hand E4
            ("F4",),                   # Right hand F4
            ("G4",),                   # Right hand G4
            
            ("G2", "B2", "D3", "G4"),  # Left hand switches to G Major Chord + Right hand G4
            ("F4",),                   # Right hand F4
            ("E4",),                   # Right hand E4
            ("D4",),                   # Right hand D4
            
            ("C3", "E3", "G3", "C4"),  # Left hand returns to C Major Chord + Right hand C4
            ("C4",),                   # Right hand C4
            ("D4",),                   # Right hand D4
            ("E4",),                   # Right hand E4
            
            ("G2", "B2", "D3", "E4"),  # Left hand G Major Chord + Right hand E4
            ("D4",),                   # Right hand D4
            ("D4",),                   # Right hand D4 (End of measure)

            # THEME A' (Last 4 Measures)
            ("C3", "E3", "G3", "E4"),  # Left hand C Major Chord + Right hand E4
            ("E4",),
            ("F4",),
            ("G4",),
            
            ("G2", "B2", "D3", "G4"),  # Left hand G Major Chord + Right hand G4
            ("F4",),
            ("E4",),
            ("D4",),
            
            ("C3", "E3", "G3", "C4"),  # Left hand C Major Chord + Right hand C4
            ("C4",),
            ("D4",),
            ("E4",),
            
            ("G2", "B2", "D3", "D4"),  # Left hand G Major Chord + Right hand D4
            ("C4",),                   # Right hand C4
            ("C3", "E3", "G3", "C4")   # GRAND FINALE: Both hands C Major Root Chord
        ]
    }
}
