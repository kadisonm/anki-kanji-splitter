import aqt.qt as qt

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
    def __init__(self, text):
        super().__init__(text)
        self.setWordWrap(True)

class Italics(qt.QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("font-style: italic;")
        self.setWordWrap(True)

class Button(qt.QPushButton):
    def __init__(self, label):
        super().__init__(label)
        self.setFixedSize(120, 30) 
        self.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)

class Br(qt.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(qt.QFrame.HLine)
        self.setFrameShadow(qt.QFrame.Sunken)

class DropdownLabel(qt.QVBoxLayout):
    def __init__(self, heading, description):
        super().__init__()

        self.dropdown = qt.QComboBox()
        self.dropdown.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)
        
        self.addWidget(H3(heading))
        self.addWidget(P(description))
        self.addWidget(self.dropdown)
        self.addWidget(Br())
        
class ButtonLabel(qt.QVBoxLayout):
    def __init__(self, heading, label, description):
        super().__init__()

        self.button = qt.QPushButton(label)
        self.button.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)
        
        self.addWidget(H3(heading))
        self.addWidget(P(description))
        self.addWidget(self.button)
        self.addWidget(Br())

class CheckBoxLabel(qt.QHBoxLayout):
    def __init__(self, description):
        super().__init__()

        self.checkbox = qt.QCheckBox()
        self.checkbox.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)
        
        self.addWidget(self.checkbox)  
        self.addWidget(P(description))
        self.addStretch()
            


