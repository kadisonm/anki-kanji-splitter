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
    def __init__(self, text):
        super().__init__(text)
        self.setFixedSize(120, 30) 
        self.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)