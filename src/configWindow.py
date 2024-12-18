import string
from xml.etree.ElementTree import tostring
from aqt.qt import *
from aqt import mw
from .config import get_config, update_config
from anki import deck_config_pb2

class ConfigWindow(QDialog):
    def __init__(self, parent):
        super(ConfigWindow, self).__init__(parent)

        self.setWindowTitle("Kanji Learner")
        self.setFixedHeight(300)
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
        explanation = QLabel("Select a deck to automatically add kanji/primitive cards to whenever a new note is created. Cards will be placed before the new note.", self)
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

        # Show selecting deck
        decks = mw.col.decks.all_names_and_ids()
        deckDropdown = QComboBox()

        deckDropdown.addItem("None", 0)

        currentDeck = "None"

        for deck in decks:
            if str(deck.id) == config["deck_id"]:
                currentDeck = deck.name
            deckDropdown.addItem(deck.name, str(deck.id))

        if currentDeck:
            deckDropdown.setCurrentText(currentDeck)
        else:
            deckDropdown.setCurrentIndex(0)

        layout.addWidget(deckDropdown, 1)

        # Scan deck
        scanLabel = QLabel("Scan deck", self)
        scanLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(scanLabel)

        explanation2 = QLabel("This will scan the deck for kanji and add new cards for any found kanji/primitives. If cards already exist, that kanji/primitive wil; be skipped.", self)
        explanation2.setWordWrap(True)
        layout.addWidget(explanation2)

        scanButton = QPushButton("Scan deck")
        scanButton.setFixedSize(120, 30) 
        layout.addWidget(scanButton)


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
            config["deck_id"] = str(deckDropdown.currentData())
            update_config(config)
            self.close()

        saveButton.clicked.connect(save_action)
        cancelButton.clicked.connect(self.close)
    
        return layout