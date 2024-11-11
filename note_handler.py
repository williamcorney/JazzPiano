import copy,threading
from playsound3 import playsound


class note_handler:
    def __init__(self):
        self.required_notes = []  # Ensure required_notes is initialized
        pass

    def midi_handling(self, mididata):
        print (self.required_notes)
        # Check if the note is on and matches the required note
        if mididata.type == "note_on" and len(self.required_notes) > 0:
            if mididata.note == self.required_notes[0]:
                self.note_on_signal.emit(mididata.note, "green")
                self.required_notes.pop(0)

                # If all notes are processed, trigger go_button_clicked
                if len(self.required_notes) == 0:
                    self.play_sound()
                    self.go_button_clicked()
            else:
                # Emit red for incorrect note
                self.note_on_signal.emit(mididata.note, "red")
                self.reset_scale()

        elif mididata.type == "note_off":
            # Handle note off
            self.note_off_signal.emit(mididata.note)

    def reset_scale(self):

        if hasattr(self, 'deepnotes') and self.deepnotes: self.required_notes = copy.deepcopy(self.deepnotes)
    def play_sound(self):
        thread = threading.Thread(target=playsound, args=('./Sounds/Correct.mp3',))
        thread.start()
        return thread
