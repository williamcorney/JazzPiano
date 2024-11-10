import random


def generate_scale(scale_type, octaves, base_offset, random_order=False, descending=False, repeat_top_note=False, scale_index=None):


    # Define the intervals for each scale type
    scales_intervals = {
        "01": [2, 2, 1, 2, 2, 2, 1],  # Major
        "02": [2, 1, 2, 2, 1, 2, 2],  # Natural Minor
        "03": [2, 1, 2, 2, 1, 3, 1],  # Harmonic Minor
        "04": [2, 1, 2, 2, 2, 2, 1]  # Melodic Minor
    }

    # Define the key signatures for major and minor scales in the order of the circle of fifths
    key_signatures_major = {
        "C Major": {"sharps": 0, "flats": 0, "notes": [], "start_note": "C"},
        "G Major": {"sharps": 1, "flats": 0, "notes": ["F#"], "start_note": "G"},
        "D Major": {"sharps": 2, "flats": 0, "notes": ["F#", "C#"], "start_note": "D"},
        "A Major": {"sharps": 3, "flats": 0, "notes": ["F#", "C#", "G#"], "start_note": "A"},
        "E Major": {"sharps": 4, "flats": 0, "notes": ["F#", "C#", "G#", "D#"], "start_note": "E"},
        "B Major": {"sharps": 5, "flats": 0, "notes": ["F#", "C#", "G#", "D#", "A#"], "start_note": "B"},
        "F# Major": {"sharps": 6, "flats": 0, "notes": ["F#", "C#", "G#", "D#", "A#", "E#"], "start_note": "F#"},
        "C# Major": {"sharps": 7, "flats": 0, "notes": ["F#", "C#", "G#", "D#", "A#", "E#", "B#"], "start_note": "C#"},
        "F Major": {"sharps": 0, "flats": 1, "notes": ["Bb"], "start_note": "F"},
        "Bb Major": {"sharps": 0, "flats": 2, "notes": ["Bb", "Eb"], "start_note": "Bb"},
        "Eb Major": {"sharps": 0, "flats": 3, "notes": ["Bb", "Eb", "Ab"], "start_note": "Eb"},
        "Ab Major": {"sharps": 0, "flats": 4, "notes": ["Bb", "Eb", "Ab", "Db"], "start_note": "Ab"},
        "Db Major": {"sharps": 0, "flats": 5, "notes": ["Bb", "Eb", "Ab", "Db", "Gb"], "start_note": "Db"},
        "Gb Major": {"sharps": 0, "flats": 6, "notes": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb"], "start_note": "Gb"},
        "Cb Major": {"sharps": 0, "flats": 7, "notes": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb", "Fb"], "start_note": "Cb"}
    }

    key_signatures_minor = {
        "A Natural Minor": {"sharps": 0, "flats": 0, "notes": [], "start_note": "A"},
        "E Natural Minor": {"sharps": 1, "flats": 0, "notes": ["F#"], "start_note": "E"},
        "B Natural Minor": {"sharps": 2, "flats": 0, "notes": ["F#", "C#"], "start_note": "B"},
        "F# Natural Minor": {"sharps": 3, "flats": 0, "notes": ["F#", "C#", "G#"], "start_note": "F#"},
        "C# Natural Minor": {"sharps": 4, "flats": 0, "notes": ["F#", "C#", "G#", "D#"], "start_note": "C#"},
        "G# Natural Minor": {"sharps": 5, "flats": 0, "notes": ["F#", "C#", "G#", "D#", "A#"], "start_note": "G#"},
        "D# Natural Minor": {"sharps": 6, "flats": 0, "notes": ["F#", "C#", "G#", "D#", "A#", "E#"],
                             "start_note": "D#"},
        "Eb Natural Minor": {"sharps": 0, "flats": 6, "notes": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb"],
                             "start_note": "Eb"},
        "Bb Natural Minor": {"sharps": 0, "flats": 5, "notes": ["Bb", "Eb", "Ab", "Db", "Gb"], "start_note": "Bb"},
        "F Natural Minor": {"sharps": 0, "flats": 4, "notes": ["Bb", "Eb", "Ab", "Db"], "start_note": "F"},
        "C Natural Minor": {"sharps": 0, "flats": 3, "notes": ["Bb", "Eb", "Ab"], "start_note": "C"},
        "G Natural Minor": {"sharps": 0, "flats": 2, "notes": ["Bb", "Eb"], "start_note": "G"},
        "D Natural Minor": {"sharps": 0, "flats": 1, "notes": ["Bb"], "start_note": "D"}
    }

    key_signatures_melodic = {
        "A Melodic Minor": {"sharps": 0, "flats": 0, "notes": [], "start_note": "A"},
        "E Melodic Minor": {"sharps": 1, "flats": 0, "notes": ["F#"], "start_note": "E"},
        "B Melodic Minor": {"sharps": 2, "flats": 0, "notes": ["F#", "C#"], "start_note": "B"},
        "F# Melodic Minor": {"sharps": 3, "flats": 0, "notes": ["F#", "C#", "G#"], "start_note": "F#"},
        "C# Melodic Minor": {"sharps": 4, "flats": 0, "notes": ["F#", "C#", "G#", "D#"], "start_note": "C#"},
        "G# Melodic Minor": {"sharps": 5, "flats": 0, "notes": ["F#", "C#", "G#", "D#", "A#"], "start_note": "G#"},
        "D# Melodic Minor": {"sharps": 6, "flats": 0, "notes": ["F#", "C#", "G#", "D#", "A#", "E#"],
                             "start_note": "D#"},
        "Eb Melodic Minor": {"sharps": 6, "flats": 0, "notes": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb"],
                             "start_note": "Eb"},
        "Bb Melodic Minor": {"sharps": 0, "flats": 5, "notes": ["Bb", "Eb", "Ab", "Db", "Gb"], "start_note": "Bb"},
        "F Melodic Minor": {"sharps": 0, "flats": 4, "notes": ["Bb", "Eb", "Ab", "Db"], "start_note": "F"},
        "C Melodic Minor": {"sharps": 0, "flats": 3, "notes": ["Bb", "Eb", "Ab"], "start_note": "C"},
        "G Melodic Minor": {"sharps": 0, "flats": 2, "notes": ["Bb", "Eb"], "start_note": "G"},
        "D Melodic Minor": {"sharps": 0, "flats": 1, "notes": ["Bb"], "start_note": "D"}
    }

    key_signatures_harmonic = {
        "A Harmonic Minor": {"sharps": 0, "flats": 0, "notes": [], "start_note": "A"},
        "E Harmonic Minor": {"sharps": 1, "flats": 0, "notes": ["F#"], "start_note": "E"},
        "B Harmonic Minor": {"sharps": 2, "flats": 0, "notes": ["F#", "C#"], "start_note": "B"},
        "F# Harmonic Minor": {"sharps": 3, "flats": 0, "notes": ["F#", "C#", "G#"], "start_note": "F#"},
        "C# Harmonic Minor": {"sharps": 4, "flats": 0, "notes": ["F#", "C#", "G#", "D#"], "start_note": "C#"},
        "G# Harmonic Minor": {"sharps": 5, "flats": 0, "notes": ["F#", "C#", "G#", "D#", "A#"], "start_note": "G#"},
        "D# Harmonic Minor": {"sharps": 6, "flats": 0, "notes": ["F#", "C#", "G#", "D#", "A#", "E#"], "start_note": "D#"},
        "Eb Harmonic Minor": {"sharps": 0, "flats": 6, "notes": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb"], "start_note": "Eb"},
        "Bb Harmonic Minor": {"sharps": 0, "flats": 5, "notes": ["Bb", "Eb", "Ab", "Db", "Gb"], "start_note": "Bb"},
        "F Harmonic Minor": {"sharps": 0, "flats": 4, "notes": ["Bb", "Eb", "Ab", "Db"], "start_note": "F"},
        "C Harmonic Minor": {"sharps": 0, "flats": 3, "notes": ["Bb", "Eb", "Ab"], "start_note": "C"},
        "G Harmonic Minor": {"sharps": 0, "flats": 2, "notes": ["Bb", "Eb"], "start_note": "G"},
        "D Harmonic Minor": {"sharps": 0, "flats": 1, "notes": ["Bb"], "start_note": "D"}
    }


    # Function to convert note name to MIDI note
    def note_name_to_midi(note_name):
        note_names = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7,
                      'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
        return note_names[note_name]

    # Function to convert MIDI note to note name
    def midi_to_note_name(midi_note):
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = int(midi_note) // 12 - 1
        note = int(midi_note) % 12
        return f"{note_names[note]}{octave}"

    # Adjust the note names based on the key signature, handling enharmonic equivalents
    def adjust_for_key_signature(note_names, key_signature):
        enharmonic_map = {
            'G#': 'Ab', 'D#': 'Eb', 'A#': 'Bb', 'C#': 'Db'
        }
        adjusted_notes = []
        for note in note_names:
            note_name = note[:-1]  # Strip the octave number
            octave = note[-1]
            if note_name in enharmonic_map and enharmonic_map[note_name] in key_signature:
                adjusted_note = enharmonic_map[note_name] + octave
                adjusted_notes.append(adjusted_note)
            else:
                adjusted_notes.append(note)
        return adjusted_notes

    # Select the key signature
    # Select the key signature
    # Circle of Fifths for Major, Natural Minor, Harmonic Minor, Melodic Minor
    circle_of_fifths_major = [
        "C Major", "G Major", "D Major", "A Major", "E Major", "B Major", "F# Major",
        "Db Major", "Ab Major", "Eb Major", "Bb Major", "F Major"
    ]

    circle_of_fifths_minor = [
        "A Natural Minor", "E Natural Minor", "B Natural Minor", "F# Natural Minor", "C# Natural Minor",
        "G# Natural Minor",
        "Eb Natural Minor", "Bb Natural Minor", "F Natural Minor", "C Natural Minor", "G Natural Minor",
        "D Natural Minor"
    ]

    circle_of_fifths_harmonic = [
        "A Harmonic Minor", "E Harmonic Minor", "B Harmonic Minor", "F# Harmonic Minor", "C# Harmonic Minor",
        "G# Harmonic Minor",
        "Eb Harmonic Minor", "Bb Harmonic Minor", "F Harmonic Minor", "C Harmonic Minor", "G Harmonic Minor",
        "D Harmonic Minor"
    ]

    circle_of_fifths_melodic = [
        "A Melodic Minor", "E Melodic Minor", "B Melodic Minor", "F# Melodic Minor", "C# Melodic Minor",
        "G# Melodic Minor",
        "Eb Melodic Minor", "Bb Melodic Minor", "F Melodic Minor", "C Melodic Minor", "G Melodic Minor",
        "D Melodic Minor"
    ]

    if random_order:
        if scale_type == "01":  # Major
            selected_key = random.choice(circle_of_fifths_major)
        elif scale_type == "02":  # Natural Minor
            selected_key = random.choice(circle_of_fifths_minor)
        elif scale_type == "03":  # Harmonic Minor
            selected_key = random.choice(circle_of_fifths_harmonic)
        elif scale_type == "04":  # Melodic Minor
            selected_key = random.choice(circle_of_fifths_melodic)
    else:
        if scale_index is not None:
            if scale_type == "01":
                selected_key = circle_of_fifths_major[scale_index % len(circle_of_fifths_major)]
            elif scale_type == "02":
                selected_key = circle_of_fifths_minor[scale_index % len(circle_of_fifths_minor)]
            elif scale_type == "03":
                selected_key = circle_of_fifths_harmonic[scale_index % len(circle_of_fifths_harmonic)]
            elif scale_type == "04":
                selected_key = circle_of_fifths_melodic[scale_index % len(circle_of_fifths_melodic)]
        else:
            selected_key = "C Major" if scale_type == "01" else "A Natural Minor"


    if scale_type == "01":
        key_sig = key_signatures_major[selected_key]
    elif scale_type == "02":
        key_sig = key_signatures_minor[selected_key]
    elif scale_type == "03":
        key_sig = key_signatures_harmonic[selected_key]
    elif scale_type == "04":
        key_sig = key_signatures_melodic[selected_key]

    if scale_type == "01":  # Major
        key_sig = key_signatures_major[selected_key]
    elif scale_type == "02":  # Natural Minor
        key_sig = key_signatures_minor[selected_key]
    elif scale_type == "03":  # Harmonic Minor
        key_sig = key_signatures_harmonic[selected_key]
    elif scale_type == "04":  # Melodic Minor
        key_sig = key_signatures_melodic[selected_key]

    start_note_name = key_sig["start_note"]
    start_note = note_name_to_midi(start_note_name)

    # Generate the scale
    intervals = scales_intervals[scale_type]
    note_names = []
    root_midi_values = []
    relative_midi_values = []

    current_note = start_note
    note_names.append(current_note)
    root_midi_values.append(current_note + base_offset)
    relative_midi_values.append(current_note)


    for _ in range(octaves):
        for interval in intervals:
            current_note += interval
            note_names.append(current_note)
            root_midi_values.append(current_note + base_offset)
            relative_midi_values.append(current_note)

    # Handle descending notes
    descending_notes = list(reversed(relative_midi_values[:-1]))  # Exclude the last note to avoid duplication
    if repeat_top_note:
        descending_notes.insert(0, current_note)  # Ensure the top note appears first in descending sequence

    if descending:
        note_names.extend(descending_notes)
        root_midi_values.extend([note + base_offset for note in descending_notes])
        relative_midi_values.extend(descending_notes)


    # Adjust the notes for the key signature
    pre_adjustment_notes = [midi_to_note_name(note + base_offset) for note in note_names]


    note_names = adjust_for_key_signature(pre_adjustment_notes, key_sig["notes"])


    result = {
        "scale_type": scale_type,
        "repeated_top_note": repeat_top_note,
        "descending": descending,
        "note_names": note_names,
        "root_midi_values": root_midi_values,
        "relative_midi_values": relative_midi_values,
        "random_order": random_order,
        "key_signature": selected_key,
        "key_signature_notes": key_sig["notes"],  # Include the specific sharps/flats
        "sharps": key_sig.get("sharps"),
        "flats": key_sig.get("flats")
    }


    return result



