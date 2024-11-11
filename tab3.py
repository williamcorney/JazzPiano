from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox, QLineEdit
import pickle


class Tab3(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize settings dictionary
        self.settings = {}

        # Create layout and widgets
        layout = QVBoxLayout(self)

        # Scale Type Combo Box
        self.scale_type_label = QLabel("Select Scale Type", self)
        layout.addWidget(self.scale_type_label)
        self.scale_type_combo = QComboBox(self)
        self.scale_type_combo.addItems(["01", "02", "03", "04"])  # Scale Types 01-04
        layout.addWidget(self.scale_type_combo)

        # Octave Combo Box
        self.octave_label = QLabel("Select Octave", self)
        layout.addWidget(self.octave_label)
        self.octave_combo = QComboBox(self)
        self.octave_combo.addItems([str(i) for i in range(1, 3)])  # Octaves 1-2
        layout.addWidget(self.octave_combo)

        # Base Offset QLineEdit
        self.base_offset_label = QLabel("Base Offset", self)
        layout.addWidget(self.base_offset_label)
        self.base_offset_edit = QLineEdit(self)
        layout.addWidget(self.base_offset_edit)

        # Random Order Check Box
        self.random_order_check = QCheckBox("Random Order", self)
        layout.addWidget(self.random_order_check)

        # Descending Check Box
        self.descending_check = QCheckBox("Descending", self)
        layout.addWidget(self.descending_check)

        # Repeat Top Note Check Box
        self.repeat_top_note_check = QCheckBox("Repeat Top Note", self)
        layout.addWidget(self.repeat_top_note_check)

        # Scale Index Combo Box
        self.scale_index_label = QLabel("Select Scale Index", self)
        layout.addWidget(self.scale_index_label)
        self.scale_index_combo = QComboBox(self)
        self.scale_index_combo.addItems([str(i) for i in range(12)])  # Scale Index 0-11
        layout.addWidget(self.scale_index_combo)

        # Status message label
        self.status_label = QLabel("", self)  # This will hold the success or error messages
        layout.addWidget(self.status_label)

        # Flag to prevent auto-save during loading
        self.is_loading = False

        # Load settings when the widget is initialized
        self.load_settings()

        # Connect signals for auto-save after settings are applied
        self.scale_type_combo.currentIndexChanged.connect(self.auto_save)
        self.octave_combo.currentIndexChanged.connect(self.auto_save)
        self.base_offset_edit.textChanged.connect(self.auto_save)
        self.random_order_check.toggled.connect(self.auto_save)
        self.descending_check.toggled.connect(self.auto_save)
        self.repeat_top_note_check.toggled.connect(self.auto_save)
        self.scale_index_combo.currentIndexChanged.connect(self.auto_save)

    def load_settings(self):
        """Load settings from a pickle file into self.settings dictionary."""
        print("Loading settings...")  # Debugging line
        try:
            with open("settings.pkl", "rb") as file:
                self.settings = pickle.load(file)
                print("Settings loaded:", self.settings)  # Debugging line

                # Set the loading flag to True to prevent auto-save triggers
                self.is_loading = True

                # Update widgets based on loaded settings
                self.apply_settings()

                # After applying settings, reset the flag
                self.is_loading = False

                self.status_label.setText("Settings loaded successfully.")
                self.status_label.setStyleSheet("color: green;")  # Green for success
        except FileNotFoundError:
            self.status_label.setText("settings.pkl not found. Using default settings.")
            self.status_label.setStyleSheet("color: red;")  # Red for error
            print("settings.pkl not found. Using default settings.")  # Debugging line
        except Exception as e:
            self.status_label.setText(f"Failed to load settings: {e}")
            self.status_label.setStyleSheet("color: red;")  # Red for error
            print("Error loading settings:", e)  # Debugging line

    def apply_settings(self):
        """Apply loaded settings to the widgets."""
        print("Applying settings...")  # Debugging line
        if 'scale_type' in self.settings:
            self.scale_type_combo.setCurrentText(self.settings['scale_type'])
        if 'octave' in self.settings:
            self.octave_combo.setCurrentText(str(self.settings['octave']))
        if 'base_offset' in self.settings:
            self.base_offset_edit.setText(str(self.settings['base_offset']))
        if 'random_order' in self.settings:
            self.random_order_check.setChecked(self.settings['random_order'])
        if 'descending' in self.settings:
            self.descending_check.setChecked(self.settings['descending'])
        if 'repeat_top_note' in self.settings:
            self.repeat_top_note_check.setChecked(self.settings['repeat_top_note'])
        if 'scale_index' in self.settings:
            self.scale_index_combo.setCurrentText(str(self.settings['scale_index']))

    def save_settings(self):
        """Save settings to pickle file."""
        print("Saving settings...")  # Debugging line
        try:
            # Get the value from base_offset_edit and convert it to an integer
            base_offset = int(
                self.base_offset_edit.text()) if self.base_offset_edit.text().isdigit() else 60  # Default to 60 if not valid

            # Update settings with the current widget values
            self.settings['scale_type'] = self.scale_type_combo.currentText()
            self.settings['octave'] = int(self.octave_combo.currentText())
            self.settings['base_offset'] = base_offset  # Save as integer
            self.settings['random_order'] = self.random_order_check.isChecked()
            self.settings['descending'] = self.descending_check.isChecked()
            self.settings['repeat_top_note'] = self.repeat_top_note_check.isChecked()
            self.settings['scale_index'] = int(self.scale_index_combo.currentText())

            # Save settings to file
            with open("settings.pkl", "wb") as file:
                pickle.dump(self.settings, file)

            self.status_label.setText("Settings saved successfully.")
            self.status_label.setStyleSheet("color: green;")  # Green for success
        except Exception as e:
            self.status_label.setText(f"Failed to save settings: {e}")
            self.status_label.setStyleSheet("color: red;")  # Red for error

    def auto_save(self):
        """Automatically save settings whenever any field is modified."""
        # Check if the active tab is the settings tab (Tab3)
        if self.parent().currentWidget() == self:
            self.save_settings()


if __name__ == "__main__":
    from main import Oralia

    oralia.main()
