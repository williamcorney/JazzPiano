from scale_generator import generate_scale
import pickle,copy

class tab1_theory:
    def __init__(self):
        # Initialize settings dictionary
        self.Settings = {}
        # Attempt to load settings
        self.load_settings()

    def load_settings(self):
        """Load settings from pickle file into self.Settings."""
        try:
            with open("settings.pkl", "rb") as file:
                self.Settings = pickle.load(file)
        except FileNotFoundError:
            print("Settings file not found. Using default settings.")
        except Exception as e:
            print(f"Error loading settings: {e}")

    def go_button_clicked(self):
        self.load_settings()
        # Get the values from self.Settings or fall back to defaults
        scale_type = self.Settings.get('scale_type', '01')  # Default to '01'
        octave = self.Settings.get('octave', 1)  # Default to octave 1
        base_offset = self.Settings.get('base_offset', 60)  # Default to MIDI value 60
        base_offset = int(base_offset)
        random_order = self.Settings.get('random_order', True)  # Default to True
        descending = self.Settings.get('descending', False)  # Default to False
        repeat_top_note = self.Settings.get('repeat_top_note', False)  # Default to False
        scale_index = self.Settings.get('scale_index', 0)  # Default to index 0

        # Call generate_scale using values from self.Settings
        result = generate_scale(scale_type, octave, base_offset,
                                random_order=random_order, descending=descending,
                                repeat_top_note=repeat_top_note,
                                scale_index=scale_index)

        # Update the key label and required notes
        self.labels['key_label'].setText(result['key_signature'])
        self.required_notes = result['root_midi_values']
        self.deepnotes = copy.deepcopy(self.required_notes)

    def reset_scale(self):
        if hasattr(self, 'deepnotes') and self.deepnotes: self.required_notes = copy.deepcopy(self.deepnotes)

# # Create an instance of tab1_theory
# theory_instance = tab1_theory()
#
# # Call the go_button_clicked method to test it
# theory_instance.go_button_clicked()
