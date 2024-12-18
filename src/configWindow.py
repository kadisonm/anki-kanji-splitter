from aqt.qt import *
from aqt import mw
from .config import get_config, update_config

class ConfigWindow(QDialog):
    def __init__(self, parent):
        super(ConfigWindow, self).__init__(parent)

        self.setWindowTitle("Kanji Learner")
        self.setFixedHeight(250)
        self.setFixedWidth(600)
        self.loaded = False

    def open(self):
        if mw.col and not self.loaded:
            self.setLayout(self.ui())
            self.loaded = True
        
        self.show()

    def close(self):
        self.hide()
    
    def ui(self):
        if not mw.col:
            return
        
        config = get_config()

        layout = QVBoxLayout()

        # Title
        titleLabel = QLabel("Kanji Learner", self)
        titleLabel.setStyleSheet("font-size: 30px; font-weight: bold;")
        layout.addWidget(titleLabel)

        # Author
        authorLabel = QLabel("Kadison McLellan", self)
        authorLabel.setStyleSheet("font-size: 12px; font-style: italic; margin-bottom: 30px")
        layout.addWidget(authorLabel)

        # Deck Selection Label
        deckLabel = QLabel("Select deck", self)
        deckLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(deckLabel)

        # Explanation
        explanation = QLabel("Select a deck to automatically scan and add kanji/primitive cards to. New cards will be placed before the card they originate from", self)
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

        # Show selecting deck
        deckNames = mw.col.decks.all_names()
        deckNames.insert(1, "None")
    
        deckDropdown = QComboBox()
        deckDropdown.addItems(deckNames)
        deckDropdown.setCurrentText(config["deck"])

        layout.addWidget(deckDropdown, 1)

        # Buttons layout (horizontal)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addSpacerItem(QSpacerItem(600, 30))
        layout.addLayout(buttonsLayout)

        # Save button
        saveButton = QPushButton("Save")
        saveButton.setFixedSize(120, 30) 
        buttonsLayout.addWidget(saveButton)

        # Close button
        cancelButton = QPushButton("Cancel")
        cancelButton.setFixedSize(120, 30) 
        buttonsLayout.addWidget(cancelButton)

        # Button actions
        def save_action():
            config["deck"] = deckDropdown.currentText()
            update_config(config)
            self.close()

        saveButton.clicked.connect(save_action)
        cancelButton.clicked.connect(self.close)
    
        return layout