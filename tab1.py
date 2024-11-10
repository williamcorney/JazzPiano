from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView,QLabel, QPushButton, QAbstractItemView)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, pyqtSignal
import os
import pickle
from tab1_gui import tab1_gui
from note_handler import note_handler
from tab1_theory import tab1_theory
class Tab1(tab1_gui, note_handler,tab1_theory):

    def __init__(self, parent_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.parent_widget = parent_widget







