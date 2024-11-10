from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView,QLabel, QPushButton, QAbstractItemView)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, pyqtSignal
import os
import pickle


class tab1_gui(QWidget):
    note_on_signal = pyqtSignal(int, str)
    note_off_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.labels, self.pixmap_item = {}, {}
        self.theorymode = None

        with open('theory.pkl', 'rb') as file:
            self.Theory = pickle.load(file)
            print(self.Theory['Theory'])

        self.setLayout(QVBoxLayout())
        self.horizontal = QHBoxLayout()
        self.layout().addLayout(self.horizontal)

        self.theory1, self.theory2, self.theory3 = QListWidget(), QListWidget(), QListWidget()
        for theory in [self.theory1, self.theory2, self.theory3]:
            self.horizontal.addWidget(theory, stretch=1)

        self.theory1.addItems(["Notes", "Scales", "Triads", "Sevenths", "Modes", "Shells"])
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

        for key, text in [('key_label', 'Key: C Major'),
                          ('inversion_label', 'Inversion: Root'),
                          ('fingering_label', 'Fingering: 1-2-3-4-5'),
                          ('score_value', 'Score: 100')]:
            label = QLabel(text)
            if key == 'key_label':
                label.setFont(QFont("Arial", 32))
            self.labels[key] = label
            self.horizontal_vertical.addWidget(label)

        self.go_button = QPushButton("Go")
        self.connect_signals()
        self.horizontal_vertical.addWidget(self.go_button)



    def theory1_clicked(self):
        self.labels['score_value'].setText("")
        self.labels['fingering_label'].clear()
        self.labels['key_label'].setText("")

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

    def connect_signals(self):
        pass
        self.note_on_signal.connect(self.insert_note)
        self.note_off_signal.connect(self.delete_note)
        self.theory1.clicked.connect(self.theory1_clicked)
        self.theory2.clicked.connect(self.theory2_clicked)
        self.theory3.clicked.connect(self.theory3_clicked)
        self.go_button.clicked.connect(self.go_button_clicked)