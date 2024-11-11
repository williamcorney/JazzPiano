import random


def generate_scale(scale_type, octaves, base_offset, random_order=False, descending=False, repeat_top_note=False, scale_index=None):




    scales_intervals = {
        "01": [2, 2, 1, 2, 2, 2, 1],
        "02": [2, 1, 2, 2, 1, 2, 2],
        "03": [2, 1, 2, 2, 1, 3, 1],
        "04": [2, 1, 2, 2, 2, 2, 1]
    }

    key_signatures_major = {
        "C Major": {"sharps": 0, "flats": 0, "notes": [], "start_note": "C"},
        "G Major": {"sharps": 1, "flats": 0, "notes": ["F♯"], "start_note": "G"},
        "D Major": {"sharps": 2, "flats": 0, "notes": ["F♯", "C♯"], "start_note": "D"},
        "A Major": {"sharps": 3, "flats": 0, "notes": ["F♯", "C♯", "G♯"], "start_note": "A"},
        "E Major": {"sharps": 4, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯"], "start_note": "E"},
        "B Major": {"sharps": 5, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯", "A♯"], "start_note": "B"},
        "F♯ Major": {"sharps": 6, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯", "A♯", "E♯"], "start_note": "F♯"},
        "C♯ Major": {"sharps": 7, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯", "A♯", "E♯", "B♯"], "start_note": "C♯"},
        "F Major": {"sharps": 0, "flats": 1, "notes": ["B♭"], "start_note": "F"},
        "B♭ Major": {"sharps": 0, "flats": 2, "notes": ["B♭", "E♭"], "start_note": "B♭"},
        "E♭ Major": {"sharps": 0, "flats": 3, "notes": ["B♭", "E♭", "A♭"], "start_note": "E♭"},
        "A♭ Major": {"sharps": 0, "flats": 4, "notes": ["B♭", "E♭", "A♭", "D♭"], "start_note": "A♭"},
        "D♭ Major": {"sharps": 0, "flats": 5, "notes": ["B♭", "E♭", "A♭", "D♭", "G♭"], "start_note": "D♭"},
        "G♭ Major": {"sharps": 0, "flats": 6, "notes": ["B♭", "E♭", "A♭", "D♭", "G♭", "C♭"], "start_note": "G♭"},
        "C♭ Major": {"sharps": 0, "flats": 7, "notes": ["B♭", "E♭", "A♭", "D♭", "G♭", "C♭", "F♭"], "start_note": "C♭"}
    }

    key_signatures_minor = {
        "A Natural Minor": {"sharps": 0, "flats": 0, "notes": [], "start_note": "A"},
        "E Natural Minor": {"sharps": 1, "flats": 0, "notes": ["F♯"], "start_note": "E"},
        "B Natural Minor": {"sharps": 2, "flats": 0, "notes": ["F♯", "C♯"], "start_note": "B"},
        "F♯ Natural Minor": {"sharps": 3, "flats": 0, "notes": ["F♯", "C♯", "G♯"], "start_note": "F♯"},
        "C♯ Natural Minor": {"sharps": 4, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯"], "start_note": "C♯"},
        "G♯ Natural Minor": {"sharps": 5, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯", "A♯"], "start_note": "G♯"},
        "D♯ Natural Minor": {"sharps": 6, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯", "A♯", "E♯"],
                             "start_note": "D♯"},
        "E♭ Natural Minor": {"sharps": 0, "flats": 6, "notes": ["B♭", "E♭", "A♭", "D♭", "G♭", "C♭"],
                             "start_note": "E♭"},
        "B♭ Natural Minor": {"sharps": 0, "flats": 5, "notes": ["B♭", "E♭", "A♭", "D♭", "G♭"], "start_note": "B♭"},
        "F Natural Minor": {"sharps": 0, "flats": 4, "notes": ["B♭", "E♭", "A♭", "D♭"], "start_note": "F"},
        "C Natural Minor": {"sharps": 0, "flats": 3, "notes": ["B♭", "E♭", "A♭"], "start_note": "C"},
        "G Natural Minor": {"sharps": 0, "flats": 2, "notes": ["B♭", "E♭"], "start_note": "G"},
        "D Natural Minor": {"sharps": 0, "flats": 1, "notes": ["B♭"], "start_note": "D"}
    }

    key_signatures_melodic = {
        "A Melodic Minor": {"sharps": 0, "flats": 0, "notes": [], "start_note": "A"},
        "E Melodic Minor": {"sharps": 1, "flats": 0, "notes": ["F♯"], "start_note": "E"},
        "B Melodic Minor": {"sharps": 2, "flats": 0, "notes": ["F♯", "C♯"], "start_note": "B"},
        "F♯ Melodic Minor": {"sharps": 3, "flats": 0, "notes": ["F♯", "C♯", "G♯"], "start_note": "F♯"},
        "C♯ Melodic Minor": {"sharps": 4, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯"], "start_note": "C♯"},
        "G♯ Melodic Minor": {"sharps": 5, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯", "A♯"], "start_note": "G♯"},
        "D♯ Melodic Minor": {"sharps": 6, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯", "A♯", "E♯"],
                             "start_note": "D♯"},
        "E♭ Melodic Minor": {"sharps": 6, "flats": 0, "notes": ["B♭", "E♭", "A♭", "D♭", "G♭", "C♭"],
                             "start_note": "E♭"},
        "B♭ Melodic Minor": {"sharps": 0, "flats": 5, "notes": ["B♭", "E♭", "A♭", "D♭", "G♭"], "start_note": "B♭"},
        "F Melodic Minor": {"sharps": 0, "flats": 4, "notes": ["B♭", "E♭", "A♭", "D♭"], "start_note": "F"},
        "C Melodic Minor": {"sharps": 0, "flats": 3, "notes": ["B♭", "E♭", "A♭"], "start_note": "C"},
        "G Melodic Minor": {"sharps": 0, "flats": 2, "notes": ["B♭", "E♭"], "start_note": "G"},
        "D Melodic Minor": {"sharps": 0, "flats": 1, "notes": ["B♭"], "start_note": "D"}
    }

    key_signatures_harmonic = {
        "A Harmonic Minor": {"sharps": 0, "flats": 0, "notes": [], "start_note": "A"},
        "E Harmonic Minor": {"sharps": 1, "flats": 0, "notes": ["F♯"], "start_note": "E"},
        "B Harmonic Minor": {"sharps": 2, "flats": 0, "notes": ["F♯", "C♯"], "start_note": "B"},
        "F♯ Harmonic Minor": {"sharps": 3, "flats": 0, "notes": ["F♯", "C♯", "G♯"], "start_note": "F♯"},
        "C♯ Harmonic Minor": {"sharps": 4, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯"], "start_note": "C♯"},
        "G♯ Harmonic Minor": {"sharps": 5, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯", "A♯"], "start_note": "G♯"},
        "D♯ Harmonic Minor": {"sharps": 6, "flats": 0, "notes": ["F♯", "C♯", "G♯", "D♯", "A♯", "E♯"], "start_note": "D♯"},
        "E♭ Harmonic Minor": {"sharps": 0, "flats": 6, "notes": ["B♭", "E♭", "A♭", "D♭", "G♭", "C♭"], "start_note": "E♭"},
        "B♭ Harmonic Minor": {"sharps": 0, "flats": 5, "notes": ["B♭", "E♭", "A♭", "D♭", "G♭"], "start_note": "B♭"},
        "F Harmonic Minor": {"sharps": 0, "flats": 4, "notes": ["B♭", "E♭", "A♭", "D♭"], "start_note": "F"},
        "C Harmonic Minor": {"sharps": 0, "flats": 3, "notes": ["B♭", "E♭", "A♭"], "start_note": "C"},
        "G Harmonic Minor": {"sharps": 0, "flats": 2, "notes": ["B♭", "E♭"], "start_note": "G"},
        "D Harmonic Minor": {"sharps": 0, "flats": 1, "notes": ["B♭"], "start_note": "D"}
    }


    def note_name_to_midi(note_name):
        note_names = {'C': 0, 'C♯': 1, 'D♭': 1, 'D': 2, 'D♯': 3, 'E♭': 3, 'E': 4, 'F': 5, 'F♯': 6, 'G♭': 6, 'G': 7,
                      'G♯': 8, 'A♭': 8, 'A': 9, 'A♯': 10, 'B♭': 10, 'B': 11}
        return note_names[note_name]

    def midi_to_note_name(midi_note):
        note_names = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']
        octave = int(midi_note) // 12 - 1
        note = int(midi_note) % 12
        return f"{note_names[note]}{octave}"

    def adjust_for_key_signature(note_names, key_signature):
        enharmonic_map = {
            'G♯': 'A♭', 'D♯': 'E♭', 'A♯': 'B♭', 'C♯': 'D♭'
        }
        adjusted_notes = []
        for note in note_names:
            note_name = note[:-1]
            octave = note[-1]
            if note_name in enharmonic_map and enharmonic_map[note_name] in key_signature:
                adjusted_note = enharmonic_map[note_name] + octave
                adjusted_notes.append(adjusted_note)
            else:
                adjusted_notes.append(note)
        return adjusted_notes


    circle_of_fifths_major = [
        "C Major", "G Major", "D Major", "A Major", "E Major", "B Major", "F♯ Major",
        "D♭ Major", "A♭ Major", "E♭ Major", "B♭ Major", "F Major"
    ]

    circle_of_fifths_minor = [
        "A Natural Minor", "E Natural Minor", "B Natural Minor", "F♯ Natural Minor", "C♯ Natural Minor",
        "G♯ Natural Minor",
        "E♭ Natural Minor", "B♭ Natural Minor", "F Natural Minor", "C Natural Minor", "G Natural Minor",
        "D Natural Minor"
    ]

    circle_of_fifths_harmonic = [
        "A Harmonic Minor", "E Harmonic Minor", "B Harmonic Minor", "F♯ Harmonic Minor", "C♯ Harmonic Minor",
        "G♯ Harmonic Minor",
        "E♭ Harmonic Minor", "B♭ Harmonic Minor", "F Harmonic Minor", "C Harmonic Minor", "G Harmonic Minor",
        "D Harmonic Minor"
    ]

    circle_of_fifths_melodic = [
        "A Melodic Minor", "E Melodic Minor", "B Melodic Minor", "F♯ Melodic Minor", "C♯ Melodic Minor",
        "G♯ Melodic Minor",
        "E♭ Melodic Minor", "B♭ Melodic Minor", "F Melodic Minor", "C Melodic Minor", "G Melodic Minor",
        "D Melodic Minor"
    ]

    if random_order:
        if scale_type == "01":
            selected_key = random.choice(circle_of_fifths_major)
        elif scale_type == "02":
            selected_key = random.choice(circle_of_fifths_minor)
        elif scale_type == "03":
            selected_key = random.choice(circle_of_fifths_harmonic)
        elif scale_type == "04":
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

    if scale_type == "01":
        key_sig = key_signatures_major[selected_key]
    elif scale_type == "02":
        key_sig = key_signatures_minor[selected_key]
    elif scale_type == "03":
        key_sig = key_signatures_harmonic[selected_key]
    elif scale_type == "04":
        key_sig = key_signatures_melodic[selected_key]

    start_note_name = key_sig["start_note"]
    start_note = note_name_to_midi(start_note_name)

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

    descending_notes = list(reversed(relative_midi_values[:-1]))
    if repeat_top_note:
        descending_notes.insert(0, current_note)

    if descending:
        note_names.extend(descending_notes)
        root_midi_values.extend([note + base_offset for note in descending_notes])
        relative_midi_values.extend(descending_notes)


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
        "key_signature_notes": key_sig["notes"],
        "sharps": key_sig.get("sharps"),
        "flats": key_sig.get("flats")
    }


    return result



