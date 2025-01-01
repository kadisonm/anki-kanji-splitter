import string
from xml.etree.ElementTree import tostring
import aqt.qt as qt
from aqt import mw
from . import config
from anki import deck_config_pb2

from .ui import *

class SettingsWindow(qt.QDialog):
    def __init__(self, parent):
        super(SettingsWindow, self).__init__(parent)

        self.setWindowTitle("Kanji Splitter")

        height = 200
        width = 400

        self.setMinimumHeight(height)
        self.setMinimumWidth(width)
        self.resize(width, height)

        self.loaded = False

    def open(self):
        if mw.col and not self.loaded:
            self.setLayout(self.loadUI())
            self.loaded = True
        
        self.show()

    def close(self):
        self.hide()
    
    def loadUI(self):
        if not mw.col:
            return
        
        data = config.get_config()

        layout = qt.QVBoxLayout()

        # Title
        layout.addWidget(H1("Kanji Splitter"))

        # Author
        layout.addWidget(Italics("By Kadison McLellan"))

        # Deck Selection Label
        layout.addWidget(H2("Select deck"))

        # Explanation
        layout.addWidget(P("Select a deck to automatically add kanji/primitive cards to whenever a new note is created. Cards will be placed before the new note."))

        # Show selecting deck
        decks = mw.col.decks.all_names_and_ids()
        deckDropdown = qt.QComboBox()
        deckDropdown.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)

        deckDropdown.addItem("None", 0)

        currentDeck = "None"

        for deck in decks:
            if deck.id == data["deck_id"]:
                currentDeck = deck.name
            deckDropdown.addItem(deck.name, deck.id)

        if currentDeck:
            deckDropdown.setCurrentText(currentDeck)
        else:
            deckDropdown.setCurrentIndex(0)

        layout.addWidget(deckDropdown, 1)

        # Scan deck
        layout.addWidget(H2("Scan deck"))
        layout.addWidget(P("This will scan the deck for kanji and add new cards for any found kanji/primitives. If cards already exist, that kanji/primitive will be skipped."))
        layout.addWidget(Button("Scan deck"))

        layout.addStretch()

        # Buttons layout (horizontal)
        buttonsLayout = qt.QHBoxLayout()
        buttonsLayout.addSpacerItem(qt.QSpacerItem(600, 30))
        layout.addLayout(buttonsLayout)

        # Save / Cancel buttons
        save = Button("Save")
        cancel = Button("Cancel")

        buttonsLayout.addWidget(save)
        buttonsLayout.addWidget(cancel)

        def save_action():
            data["deck_id"] = deckDropdown.currentData()
            config.update_config(data)
            self.close()

        save.clicked.connect(save_action)
        cancel.clicked.connect(self.close)
        
        save.setFocusPolicy(qt.Qt.FocusPolicy.ClickFocus)
    
        return layout