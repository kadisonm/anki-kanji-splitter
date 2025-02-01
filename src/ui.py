import textwrap
import aqt.qt as qt
from aqt.theme import theme_manager

class H1(qt.QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("font-size: 30px; font-weight: bold;")
        self.setWordWrap(True)

class H2(qt.QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.setWordWrap(True)

class H3(qt.QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.setWordWrap(True)

class Bold(qt.QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("font-weight: bold;")
        self.setWordWrap(True)

class P(qt.QLabel):
    def __init__(self, text, center = False):
        super().__init__(text)
        self.setWordWrap(True)

        if center == True:
            self.setAlignment(qt.Qt.AlignmentFlag.AlignCenter)

class Logo(qt.QVBoxLayout):
    def __init__(self, size):
        super().__init__()

        if theme_manager.night_mode:
            pixmap = qt.QPixmap("src/resources/icons/logo_night.png") 
        else:
            pixmap = qt.QPixmap("src/resources/icons/logo_light.png") 
       
        label = qt.QLabel()
        scaledPixmap = pixmap.scaledToWidth(size)
        label.setPixmap(scaledPixmap)
        label.setAlignment(qt.Qt.AlignmentFlag.AlignCenter)

        self.addWidget(label)

class Italics(qt.QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("font-style: italic;")
        self.setWordWrap(True)

class GroupBox(qt.QGroupBox):
    def __init__(self, text):
        super().__init__(text)
        
        self.layout = qt.QVBoxLayout()

        self.setLayout(self.layout)

class Button(qt.QPushButton):
    def __init__(self, label):
        super().__init__(label)
        self.setFixedSize(120, 30) 
        self.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)

class Br(qt.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(qt.QFrame.Shape.HLine)
        self.setFrameShadow(qt.QFrame.Shadow.Sunken)

class DropdownLabel(qt.QHBoxLayout):
    def __init__(self, description, tooltip = None):
        super().__init__()

        self.dropdown = qt.QComboBox()
        self.dropdown.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)
        
        self.addWidget(P(description))

        self.addStretch()
        self.addWidget(self.dropdown)
        
        if tooltip:
            self.addWidget(Tooltip(tooltip))

class ButtonLabel(qt.QHBoxLayout):
    def __init__(self, description, button, tooltip = None):
        super().__init__()

        self.button = qt.QPushButton(button)
        self.button.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)

        self.addWidget(P(description))

        self.addStretch()
        self.addWidget(self.button)

        if tooltip:
            self.addWidget(Tooltip(tooltip))

class CheckBoxLabel(qt.QHBoxLayout):
    def __init__(self, description):
        super().__init__()

        self.checkbox = qt.QCheckBox()
        self.checkbox.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)

        self.isChecked = self.checkbox.isChecked
        self.setChecked = self.checkbox.setChecked
        
        self.addWidget(self.checkbox)  
        self.addWidget(P(description))
        self.addStretch()

class Tooltip(qt.QToolButton):
    def __init__(self, text):
        super().__init__()
        
        if theme_manager.night_mode:
            self.setIcon(qt.QIcon("src/resources/icons/help_night.svg"))
        else:
            self.setIcon(qt.QIcon("src/resources/icons/help_light.svg"))

        self.setStyleSheet("border: none;")

        wrappedText = "\n".join(textwrap.wrap(text, width=40))

        self.setToolTip(wrappedText)

class MessageBox(qt.QMessageBox):
    def __init__(self, title, label):
        super().__init__()

        self.setWindowTitle(title)
        self.setText(label)
        
class ConfirmationBox(qt.QMessageBox):
    def __init__(self, label):
        super().__init__()

        self.setWindowTitle("Confirm Action")
        self.setText(label)
        self.setStandardButtons(qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No)
        self.setDefaultButton(qt.QMessageBox.StandardButton.Yes)
        
class SettingsDialog(qt.QDialog):
    def __init__(self, title):
        super(SettingsDialog, self).__init__()

        self.setWindowTitle(title)

        self.setMinimumHeight(200)
        self.setMinimumWidth(400)

        layout = qt.QVBoxLayout(self)

        self.heading = qt.QVBoxLayout()
        layout.addLayout(self.heading)

        # Tabs
        self.tabs = qt.QTabWidget()
        layout.addWidget(self.tabs)

        # Save / close buttons
        buttonsLayout = qt.QHBoxLayout()
        buttonsLayout.addStretch()
        layout.addLayout(buttonsLayout)

        save = Button("Save")
        cancel = Button("Cancel")

        buttonsLayout.addWidget(save)
        buttonsLayout.addWidget(cancel)
            
        save.clicked.connect(self.save_action)
        cancel.clicked.connect(self.close_action)
        
        save.setFocusPolicy(qt.Qt.FocusPolicy.ClickFocus)

    def save_action(self):
        self.close()

    def close_action(self):
        self.close()
