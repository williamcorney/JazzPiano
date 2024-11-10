from scale_generator import generate_scale

class tab1_theory:
    def __init__(self):
        pass

    def go_button_clicked(self):
        result = generate_scale('01',1,60, random_order=True)
        self.labels['key_label'].setText(result['key_signature'])

        self.required_notes = result['root_midi_values']

# # Create an instance of tab1_theory
# theory_instance = tab1_theory()
#
# # Call the go_button_clicked method to test it
# theory_instance.go_button_clicked()
