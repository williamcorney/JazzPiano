

class note_handler:
    def __init__(self):
        pass
    def midi_handling(self, mididata):

        if mididata.type == "note_on":
            self.note_on_signal.emit(mididata.note, "green")

        if mididata.type == "note_off":
            self.note_off_signal.emit(mididata.note)
    #