from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView,QLabel, QPushButton, QAbstractItemView)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, pyqtSignal
import pickle,random,copy,os,time
import threading
from playsound3 import playsound

def play_sound():
    thread = threading.Thread(target=playsound, args=('./sounds/Correct.mp3',))
    thread.start()
    return thread

class Tab1(QWidget):
    note_on_signal = pyqtSignal(int, str)
    note_off_signal = pyqtSignal(int)
    def __init__(self, parent_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.load_data()
        self.init_vars()
        self.parent_widget = parent_widget
        self.init_ui()
        self.connect_signals()
        self.invnumber = 0
    def load_data(self):
        with open('theory.pkl', 'rb') as file:
            self.Theory = pickle.load(file)
            print (self.Theory['Theory'])
        # with open('settings.pkl', 'rb') as file:
        #     self.Settings = pickle.load(file)
    def init_vars(self):
        self.labels, self.pixmap_item, self.Theory["Stats"] = {}, {}, {}
        self.required_notes, self.pressed_notes = [], []
        self.score, self.number, self.lastnote, self.index = 0, 0, 0, 0
        self.previous_scale, self.theorymode, self.correct_answer, self.correct_key = None, None, None, None
    def init_ui(self):
        self.setLayout(QVBoxLayout())
        self.horizontal = QHBoxLayout()
        self.layout().addLayout(self.horizontal)
        self.theory1, self.theory2, self.theory3 = QListWidget(), QListWidget(), QListWidget()
        for theory in [self.theory1, self.theory2, self.theory3]:self.horizontal.addWidget(theory, stretch=1)
        self.theory1.addItems(["Notes", "Scales", "Triads", "Sevenths", "Modes", "Shells"    ])
        self.theory2.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.Scene = QGraphicsScene()
        self.BackgroundPixmap = QPixmap("./Images/Piano/keys.png")
        self.BackgroundItem = QGraphicsPixmapItem(self.BackgroundPixmap)
        self.Scene.addItem(self.BackgroundItem)
        self.View = QGraphicsView(self.Scene)
        self.View.setFixedSize(self.BackgroundPixmap.size())
        self.View.setSceneRect(0, 0, self.BackgroundPixmap.width(), self.BackgroundPixmap.height())
        self.View.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.View.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout().addWidget(self.View)
        self.horizontal_vertical = QVBoxLayout()
        self.horizontal.addLayout(self.horizontal_vertical, 2)
        self.init_labels()
        self.go_button = QPushButton("Go")
        self.horizontal_vertical.addWidget(self.go_button)
    def init_labels(self):
        for key in ['key_label', 'inversion_label', 'fingering_label', 'score_value']:
            label = QLabel("")
            if key == 'key_label':
                label.setFont(QFont("Arial", 32))
            self.labels[key] = label
            self.horizontal_vertical.addWidget(label)
    def connect_signals(self):
        self.note_on_signal.connect(self.insert_note)
        self.note_off_signal.connect(self.delete_note)
        self.theory1.clicked.connect(self.theory1_clicked)
        self.theory2.clicked.connect(self.theory2_clicked)
        self.theory3.clicked.connect(self.theory3_clicked)
        self.go_button.clicked.connect(self.go_button_clicked)
    def midi_handling(self, mididata):
        if self.parent_widget.currentIndex() == 1: self.parent_widget.widget(1).midiprocessor(mididata)
        if self.parent_widget.currentIndex() == 0: self.note_handler(mididata)
    def note_handler(self, mididata):
        if mididata.type == "note_off":
            self.note_off_signal.emit(mididata.note)
            self.pressed_notes.remove(mididata.note)
        if mididata.type == "note_on":
            handled = False
            match self.theorymode:
                case "Notes":
                    if mididata.note % 12 == self.required_notes[0]:
                        self.note_on_signal.emit(mididata.note, "green")
                        self.required_notes.pop(0)
                        if len(self.required_notes) == 0:
                            play_sound()

                            self.go_button_clicked()
                        handled = True
                case "Scales" | "Modes":
                    if mididata.note == self.required_notes[0]:
                        self.note_on_signal.emit(mididata.note, "green")
                        self.required_notes.pop(0)
                        if len(self.required_notes) == 0:
                            play_sound()
                            self.go_button_clicked()
                        handled = True
                    else:self.reset_scale()
                case "Triads" | "Sevenths" | "Shells":
                    if mididata.note in self.required_notes:
                        self.note_on_signal.emit(mididata.note, "green")
                        self.pressed_notes.append(mididata.note)
                        if len(self.pressed_notes) >= len(self.required_notes):
                            play_sound()
                            self.go_button_clicked()
                        handled = True
            if not handled:self.note_on_signal.emit(mididata.note, "red")
    def go_button_clicked(self):
        self.get_theory_items()

    def theory1_clicked(self):
        self.labels['score_value'].setText("")
        self.labels['fingering_label'].clear()
        self.labels['key_label'].setText("")
        self.Theory['Stats'] = {}
        self.theory2.clear()
        self.theory3.clear()
        self.theorymode = self.theory1.selectedItems()[0].text()
        theory_items = {
            "Notes": ["Naturals", "Sharps", "Flats"],
            "Scales": ["Major", "Minor", "Harmonic Minor", "Melodic Minor"],
            "Triads": ["Major", "Minor"],
            "Sevenths": ["Maj7", "Min7", "7", "Dim7", "m7f5"],
            "Modes": ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"],
            "Shells": ["Major", "Minor", "Dominant"]
        }

        if self.theorymode in theory_items:
            self.theory2.addItems(theory_items[self.theorymode])

    def theory2_clicked(self):
        self.Theory['Stats'] = {}
        self.theory3.clear()
        self.theory2list = [item.text() for item in self.theory2.selectedItems()]

        theory3_items = {
            "Notes": [],
            "Scales": ["Right", "Left"],
            "Triads": ["Root", "First", "Second"],
            "Sevenths": ["Root", "First", "Second", "Third"],
            "Modes": [],
            "Shells": ["3/7", "7/3"]
        }

        if self.theorymode in theory3_items:
            self.theory3.addItems(theory3_items[self.theorymode])

    def theory3_clicked(self):
        modes_requiring_list = {"Notes", "Scales", "Triads", "Sevenths", "Shells"}
        if self.theorymode in modes_requiring_list: self.theory3list = [item.text() for item in self.theory3.selectedItems()]

    def get_theory_items(self):
        if not hasattr(self, 'theorymode') or not hasattr(self, 'theory2list'): return
        if self.theorymode not in ["Notes", "Modes"] and not hasattr(self, 'theory3list'):return
        self.get_random_values()
        if self.theorymode in ["Scales", "Triads", "Sevenths", "Modes", "Shells"]:
            while self.current_scale == self.previous_scale: self.get_random_values()
            self.previous_scale = self.current_scale
        if self.letter not in self.Theory["Stats"]:self.Theory["Stats"][str(self.letter)] = 0
        match self.theorymode:
            case "Notes":
                self.required_notes.clear()
                self.required_notes.append (self.int)
                if self.type == "Flats":scale_text = self.Theory["Enharmonic"][self.int]
                else:scale_text = self.Theory["Chromatic"][self.int]
                self.labels['key_label'].setText(scale_text)
            case "Scales":
                if self.type == "Harmonic Minor":self.required_notes = self.generate_harmonic_minor()
                else: self.required_notes = self.midi_note_scale_generator(self.Theory["Scales"][self.type][self.int],octaves=1,base_note=60)
                self.labels['key_label'].setText(self.current_scale)
                if hasattr(self, 'theory3list') and self.theory3list[0] == "Left":
                    self.required_notes = (self.midi_note_scale_generator((self.Theory["Scales"][self.type][self.int]),octaves=1,base_note=48))
                    self.labels['fingering_label'].setText(str(self.Theory['Fingering'][self.int][self.current_scale]['Left']))

                else:
                    self.labels['fingering_label'].setText(str(self.Theory['Fingering'][self.int][self.current_scale]['Right']))
                    incidentals = self.Theory["Theory"][self.type][self.letter]
                    self.labels['inversion_label'].setText(' '.join(map(str, incidentals)))

            case "Triads":
                self.set_chord_notes(self.Theory["Triads"])
                self.labels['key_label'].setText(f"{self.letter} {self.type} {self.inv}")
            case "Sevenths":
                self.set_chord_notes(self.Theory["Sevenths"])
                self.labels['key_label'].setText(f"{self.letter} {self.type} {self.inv}")
            case "Modes":
                self.required_notes = self.midi_note_scale_generator(self.Theory["Modes"][self.letter][self.type],octaves=1,base_note=60)
                self.labels['key_label'].setText(self.current_scale)
            case "Shells":
                self.set_shell_notes()
                self.labels['key_label'].setText(f"{self.current_scale} 7th")
        self.deepnotes = copy.deepcopy(self.required_notes)
    def generate_harmonic_minor(self):
        ascending_notes = self.midi_note_scale_generator(self.Theory["Scales"]["Harmonic Minor"][self.int],octaves=1,base_note=60,include_descending=False)
        descending_notes = self.midi_note_scale_generator(self.Theory["Scales"]["Minor"][self.int],octaves=1,base_note=60, include_descending=False)[::-1]  # Reverse to get descending notes only
        return ascending_notes[:-1] + descending_notes
    def set_shell_notes(self):
        # if not hasattr(self, 'theory3list'): return
        shell_notes = self.Theory["Shells"][self.type][self.current_scale]
        if self.theory3list[0] == "7/3": self.required_notes = shell_notes[1]
        else: self.required_notes = shell_notes[0]
        self.labels['inversion_label'].setText(self.theory3.currentItem().text())
        self.labels['key_label'].setText(f'{self.current_scale} 7th')
    def set_chord_notes(self, chord_type):

        self.required_notes = self.midi_note_scale_generator(chord_type[self.current_scale][self.inv],octaves=1,base_note=60,include_descending=False)
        self.current_scale = f"{self.letter} {self.type} Root"  # Use self.letter and self.type directly to avoid duplications
    def midi_note_scale_generator(self, notes, octaves=1, base_note=60, repeat_middle=False, include_descending=True):
        adjusted_notes = [note + base_note for note in notes]
        extended_notes = adjusted_notes[:]
        for octave in range(1, octaves): extended_notes.extend([note + 12 * octave for note in adjusted_notes[1:]])
        if include_descending:
            reversed_notes = extended_notes[::-1] if repeat_middle else extended_notes[:-1][::-1]
            extended_notes.extend(reversed_notes)
        return extended_notes
    def get_random_values(self):
        if not hasattr(self, 'theorymode') or not hasattr(self, "theory2list"): return
        def set_common_values(int_range, scale_key):
            self.int = random.choice(int_range)
            while self.lastnote == self.int: self.int = random.choice(int_range)
            circle = [0, 5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7]
            self.int = circle[self.number]
            self.number +=1
            if self.number == 12: self.number = 0
            self.letter = self.Theory[scale_key][self.int]
            self.lastnote = self.int
            self.type = random.choice(self.theory2list)
            self.current_scale = f"{self.letter} {self.type}"
        match self.theorymode:
            case "Notes":
                self.type = random.choice(self.theory2list)
                self.notes = self.Theory["Notes"][self.type]
                self.int = random.choice(self.notes)
                while self.lastnote == self.int:self.int = random.choice(self.notes)
                self.letter = self.Theory["Chromatic"][self.int]
                self.lastnote = self.int
            case "Scales":
                set_common_values([0, 2, 4, 5, 7, 9, 11], "Enharmonic")
            case "Modes":
                set_common_values(range(12), "Enharmonic")
            case "Triads" | "Sevenths" | "Shells":
                set_common_values(range(12), "Enharmonic")
                if self.theorymode in ["Triads", "Sevenths"]:
                    #if self.invnumber > 1:self.invnumber = 0
                    #invcircle = ["Third","First"]
                    # self.inv = invcircle[self.invnumber]
                    # self.invnumber += 1
                    self.inv = random.choice(self.theory3list)
    def reset_scale(self):
        if hasattr(self, 'deepnotes') and self.deepnotes: self.required_notes = copy.deepcopy(self.deepnotes)
    def insert_note(self, note, color):
        self.xcord = self.Theory["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
        self.pixmap_item[note] = QGraphicsPixmapItem(QPixmap("./Images/Piano/key_" + color + self.Theory["NoteFilenames"][note % 12]))
        self.pixmap_item[note].setPos(self.xcord, 0)
        current_scene = self.pixmap_item[note].scene()
        if current_scene: current_scene.removeItem(self.pixmap_item[note])
        self.Scene.addItem(self.pixmap_item[note])
    def delete_note(self, note):
        if note in self.pixmap_item:
            if self.pixmap_item[note].scene():self.pixmap_item[note].scene().removeItem(self.pixmap_item[note])
            del self.pixmap_item[note]
