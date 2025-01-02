import aqt.qt as qt
import aqt

from . import config
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
        if aqt.mw.col and not self.loaded:
            self.setLayout(self.loadUI())
            self.loaded = True
        
        self.show()

    def close(self):
        self.hide()
    
    def loadUI(self):
        if not aqt.mw.col:
            return
        
        data = config.get_config()

        layout = qt.QVBoxLayout()

        # Title
        layout.addWidget(H1("Kanji Splitter"))

        # Author
        layout.addWidget(Italics("By Kadison McLellan"))
        layout.addWidget(Br())

        # Selecting deck
        decks = aqt.mw.col.decks.all_names_and_ids()
  
        deckDropdownLayout = DropdownLabel(
            "Select deck",
            "Select a deck to automatically add kanji/primitive cards to whenever a new note is created. Cards will be placed before the new note."
        )

        deckDropdown = deckDropdownLayout.dropdown

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

        layout.addLayout(deckDropdownLayout)

        # Scan deck
        layout.addLayout(
            ButtonLabel(
                "Scan deck", 
                "Scan", 
                "This will scan the deck for kanji and add new cards for any found kanji/primitives. If cards already exist, that kanji/primitive will be skipped."
        ))

        # Clear deck
        layout.addLayout(
            ButtonLabel(
                "Clear deck", 
                "Clear", 
                "This will delete any cards created by this plugin inside your deck. (This will not delete the original cards)"
        ))

        # Note Options
        layout.addWidget(H3("Note options"))
        layout.addWidget(P("This will not delete existing notes but may require a rescan to fix missing fields."))

        noteLayout = qt.QHBoxLayout()

        # Front
        frontLayout = qt.QVBoxLayout()
        frontLayout.addWidget(Bold("Front"))
        frontLayout.addLayout(CheckBoxLabel("Show kanji"))
        frontLayout.addLayout(CheckBoxLabel("Show keyword"))
        frontLayout.addLayout(CheckBoxLabel("Show strokes"))
        frontLayout.addLayout(CheckBoxLabel("Show drawing canvas"))
        frontLayout.addLayout(CheckBoxLabel("Show dictionary links"))
        frontLayout.addStretch()

        # Back
        backLayout = qt.QVBoxLayout()
        backLayout.addWidget(Bold("Back"))
        backLayout.addLayout(CheckBoxLabel("Show kanji"))
        backLayout.addLayout(CheckBoxLabel("Show keyword"))
        backLayout.addLayout(CheckBoxLabel("Show strokes"))
        backLayout.addLayout(CheckBoxLabel("Show front canvas preview"))
        backLayout.addLayout(CheckBoxLabel("Show dictionary links"))
        backLayout.addStretch()
        
        noteLayout.addLayout(frontLayout)
        noteLayout.addLayout(backLayout)
        layout.addLayout(noteLayout)

        layout.addWidget(Br())

        # Save / Cancel buttons
        layout.addStretch()
        buttonsLayout = qt.QHBoxLayout()
        buttonsLayout.addStretch()
        layout.addLayout(buttonsLayout)

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