from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QRadioButton, QButtonGroup, QLabel, QPushButton, QListWidgetItem
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import QSize, QTimer, Qt
import sqlite3
import random, pickle

class Tab2(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

         # self.tune = ['D4', 'G4', 'B4', 'G4', 'B4', 'A4', 'G4', 'E4', 'D4', 'D4', 'G4', 'B4', 'G4', 'B4', 'A4', 'D5', 'B4', 'D5', 'B4', 'D5', 'B4', 'G4', 'D4', 'E4', 'G4', 'G4', 'E4', 'D4', 'D4', 'G4', 'B4', 'G4', 'B4', 'A4', 'G4']
        self.tune =   ['A4', 'G4', 'A4', 'G4', 'A4', 'G4', 'A4', 'G4', 'A4', 'C5', 'B4', 'C5', 'C5', 'B4', 'A4', 'B4', 'A4', 'B4', 'A4', 'B4', 'C5', 'B4', 'A4', 'G4', 'A4', 'G4', 'A4', 'G4', 'A4', 'G4', 'A4', 'C5', 'B4', 'B4', 'C5', 'C5', 'B4', 'A4', 'B4', 'A4', 'B4', 'A4', 'B4', 'C5', 'B4']

        #
        # self.tune =  ['C4', 'C4', 'G4', 'G4', 'A4', 'A4', 'G4', 'F4', 'F4', 'E4', 'E4', 'D4', 'D4', 'C4', 'G4', 'G4', 'F4',
        #         'F4', 'E4', 'E4', 'D4', 'G4', 'G4', 'F4', 'F4', 'E4', 'E4', 'D4', 'C4', 'C4', 'G4', 'G4', 'A4', 'A4',
        #         'G4', 'F4', 'F4', 'E4', 'E4', 'D4', 'D4', 'C4']

        self.last_correct_answer = None
        self.mode = "notes"
        self.difficultylevel = "Easy"
        self.horizontal1 = QHBoxLayout()
        self.horizontal2 = QHBoxLayout()
        self.theory4 = QListWidget()
        self.theory4.clicked.connect(self.theory4_clicked)
        self.score = 0
        self.theory5 = QListWidget()
        self.theory5.clicked.connect(self.theory5_clicked)
        self.horizontal1.addWidget(self.theory4)
        self.horizontal1.addWidget(self.theory5)
        self.theory4.addItems(['Notes', 'Keys', 'Tunes'])  # Added 'Tunes' category
        self.theory6 = QListWidget()
        self.theory6.clicked.connect(self.theory6_clicked)
        self.horizontal1.addWidget(self.theory6)
        self.signaturetype = "Major"
        self.question_label = QLabel("")  # Display the image of the note
        self.note_label = QLabel("")  # Label to display note count
        self.note_label2 = QLabel("222")
        self.key_label = QLabel("Unused")
        self.key_label.setFont(QFont("Arial", 32))
        self.inversion_label = QLabel("")
        self.fingering_label = QLabel("Unused")
        self.score_label = QLabel("Score :")
        self.score_value = QLabel("0")
        self.go_button = QPushButton("Go")
        self.horizontal1_vertical = QVBoxLayout()
        self.horizontal1.addLayout(self.horizontal1_vertical)
        self.horizontal2_vertical = QVBoxLayout()
        self.horizontal2.addLayout(self.horizontal2_vertical)
        self.horizontal1_vertical.addWidget(self.key_label)
        self.horizontal1_vertical.addWidget(self.inversion_label)
        self.horizontal1_vertical.addWidget(self.fingering_label)
        self.horizontal1_vertical.addWidget(self.score_value)
        self.horizontal1_vertical.addWidget(self.go_button)
        self.go_button.clicked.connect(self.load_quiz)
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.horizontal1)
        self.layout.addLayout(self.horizontal2)
        self.option_buttons = []
        self.button_layout = QHBoxLayout()  # Layout to hold question_label and note_label
        self.button_layout.addWidget(self.question_label)
        self.button_layout.addWidget(self.note_label)
        self.button_layout.addWidget(self.note_label2)# Adding note_label next to question_label
        self.layout.addLayout(self.button_layout)  # Adding the button_layout to the main layout
        self.vertical_layout1 = QVBoxLayout()
        self.vertical_layout2 = QVBoxLayout()
        self.button_layout.addLayout(self.vertical_layout1)
        self.button_layout.addLayout(self.vertical_layout2)
        for i in range(4):
            button = QPushButton(self)
            button.setFixedHeight(50)
            button.setFixedWidth(200)
            button.setStyleSheet("""
                       font-size: 24px;
                       background-color: green;
                       border-radius: 8px;
                       border: 2px solid black;
                   """)
            if i < 2:
                self.vertical_layout1.addWidget(button)
            else:
                self.vertical_layout2.addWidget(button)
            self.option_buttons.append(button)
        with open('theory.pkl', 'rb') as file:
            self.Theory = pickle.load(file)
        # with open('settings.pkl', 'rb') as file:
        #     self.Settings = pickle.load(file)


    def theory4_clicked(self):
            self.theory5.clear()
            self.theorymode = self.theory4.selectedItems()[0].text()
            match self.theorymode:
                case "Notes":
                    self.theory5.addItems(["Treble", "Bass"])
                    self.mode = "notes"
                case "Keys":
                    self.mode = "keys"
                    self.theory5.addItems(["Key Identification"])
                case "Tunes":
                    self.mode = "tunes"
                    self.current_tune_index = 0  # Initialize the current tune index
                    self.load_tune()

    def load_tune(self):
        if self.current_tune_index >= len(self.tune):
            self.question_label.setText("END")
            self.question_label.setFont(QFont("Arial", 32))
            self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.note_label.clear()
        else:
            current_note_full = self.tune[self.current_tune_index]
            current_note = current_note_full.split(" ")[0]
            count = 1
            for i in range(self.current_tune_index + 1, len(self.tune)):
                if self.tune[i].split(" ")[0] == current_note:
                    count += 1
                else:
                    break
            display_note = f"x{count}" if count > 1 else ""
            self.note_label.setText(display_note)

            image_path = f"/Users/williamcorney/PycharmProjects/Oralia5/Images/Notes/Treble/{current_note}.png"
            print(f"Displaying image: {image_path}")
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.5), int(pixmap.height() * 0.5),
                                          Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.question_label.setPixmap(scaled_pixmap)

    def theory5_clicked(self):
        self.clefftype = self.theory5.selectedItems()[0].text()
        self.theory6.clear()
        self.theory6.addItems(["Easy", "Advanced"])

    def theory6_clicked(self):
        self.difficultylevel = self.theory6.selectedItems()[0].text()

    def database_lookup(self, query):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute(query)
        response = cursor.fetchall()
        conn.close()
        return response

    def generate_quiz(self, last_correct_answer=None):
        if not hasattr(self, 'clefftype'):
            return
        if self.mode == 'notes':
            query = f"SELECT note_file_name, note_display_name, note_clef, note_file_name2, difficulty FROM notes WHERE note_clef = '{self.clefftype}' AND difficulty = '{self.difficultylevel}'"
        else:
            query = f"SELECT signature_filename, signature_displayname FROM signatures WHERE signature_type = '{self.signaturetype}' AND difficulty = '{self.difficultylevel}'"
        rows = self.database_lookup(query)
        if last_correct_answer:
            rows = [row for row in rows if row[0] != last_correct_answer]
        try:
            rows
        except NameError:
            return
        correct_row = random.choice(rows)
        if self.mode == 'notes':
            correct_answer = {
                "answer_image": correct_row[0],
                "note_display_name": correct_row[1],
                "note_file_name2": correct_row[3]  # Use the fourth item for notes
            }
        else:  # mode == 'signatures'
            correct_answer = {
                "answer_image": correct_row[0],
                "note_display_name": correct_row[1]
            }
        remaining_rows = [row for row in rows if row[1] != correct_row[1]]
        try:
            wrong_rows = random.sample(remaining_rows, 3)
        except:
            print('Error occurred at this place in code')
        try:
            wrong_rows
        except NameError:
            return
        wrong_answers = {
            "wrong_answer_1": {
                "answer_image": wrong_rows[0][0],
                "note_display_name": wrong_rows[0][1]
            },
            "wrong_answer_2": {
                "answer_image": wrong_rows[1][0],
                "note_display_name": wrong_rows[1][1]
            },
            "wrong_answer_3": {
                "answer_image": wrong_rows[2][0],
                "note_display_name": wrong_rows[2][1]
            }
        }
        return {"correct_answer": correct_answer, "wrong_answers": wrong_answers}

    def load_quiz(self):
        if not hasattr(self, 'clefftype'):
            return
        self.quiz = self.generate_quiz(self.last_correct_answer)
        if self.mode == 'notes':
            image_base_path = f"/Users/williamcorney/PycharmProjects/Oralia4.5/Images/Notes/{self.clefftype}/"
        else:
            image_base_path = "/Users/williamcorney/PycharmProjects/Oralia4.5/Images/Signatures/"
        image_path = image_base_path + self.quiz['correct_answer']['answer_image']
        #self.question_image.clear()
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.5), int(pixmap.height() * 0.5), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.question_label.setPixmap(scaled_pixmap)
        options = [self.quiz['correct_answer']['note_display_name']]
        options.extend([self.quiz['wrong_answers'][key]['note_display_name'] for key in self.quiz['wrong_answers']])
        random.shuffle(options)
        for i, option in enumerate(options):
            self.option_buttons[i].setText(option)
            try:
                self.option_buttons[i].clicked.disconnect()
            except TypeError:
                pass
            self.option_buttons[i].clicked.connect(lambda checked, opt=option: self.check_answer(opt, self.quiz['correct_answer']['note_display_name']))
        self.last_correct_answer = self.quiz['correct_answer']['answer_image']

    def check_answer(self, selected, correct):
        if selected == correct:
            result_image = "correct.png"
            self.increment_score()
            QTimer.singleShot(500, self.load_next_tune if self.mode == 'tunes' else self.load_quiz)
        else:
            result_image = "incorrect.png"
            self.decrement_score(2)
        result_image_path = "/Users/williamcorney/PycharmProjects/Oralia5/Images/Notes/Treble/" + result_image
        pixmap = QPixmap(result_image_path)
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.3), int(pixmap.height() * 0.3), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.question_image.setPixmap(scaled_pixmap)

    def load_next_tune(self):
        self.current_tune_index += 1
        self.load_tune()

    def midiprocessor(self, mididata):
        if mididata.type == "note_on":
            pressednote1 = self.Theory["Chromatic"][mididata.note % 12]
            pressednote2 = mididata.note // 12 - 1
            pressednote = f"{pressednote1}{pressednote2}"

            if self.mode == 'tunes':
                expected_note_full = self.tune[self.current_tune_index]
                expected_note = expected_note_full.split(" ")[0]
                print(f"Pressed note: {pressednote}, Expected note: {expected_note}")

                if pressednote == expected_note:
                    self.increment_score()
                    self.display_feedback_image("correct")

                    count = 1
                    for i in range(self.current_tune_index + 1, len(self.tune)):
                        if self.tune[i].split(" ")[0] == pressednote:
                            count += 1
                        else:
                            break

                    if count > 1:
                        self.note_label.setText(f"x{count - 1}")
                        self.tune[self.current_tune_index + 1] = f"{pressednote} x{count - 1}"
                        self.current_tune_index += 1
                    else:
                        self.note_label.setText("x1")
                        self.current_tune_index += 1
                        QTimer.singleShot(500, self.load_tune)  # Ensure image updates here
                else:
                    self.decrement_score(2)
                    self.display_feedback_image("incorrect")
            else:
                self.check_answer(pressednote, self.quiz['correct_answer']['note_file_name2'])

    def increment_score(self, points=1):
        self.score += points
        self.score_value.setText(f"Score: {self.score}")

    def decrement_score(self, points=1):
        self.score -= points
        self.score_value.setText(f"Score: {self.score}")

    def display_feedback_image(self, result):
        if result == "correct":
            print ('test')
            image_path = "/Users/williamcorney/PycharmProjects/Oralia5/Images/Notes/Treble/correct.png"
        else:
            image_path = "/Users/williamcorney/PycharmProjects/Oralia5/Images/Notes/Treble/incorrect.png"

        print(f"Displaying feedback image: {image_path}")  # Print the full path and file name
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.3), int(pixmap.height() * 0.3),
                                      Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.note_label2.setPixmap(scaled_pixmap)
        self.note_label2.update()
