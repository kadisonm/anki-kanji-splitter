# To improve readability element variables are prefixed with an abreviation
# dd_ = dropdown
# b _ = button
# cb_ = checkbox

from tabnanny import check
import aqt.qt as qt
import aqt

from . import config
from .ui import *
from . import model
from . import deck

class SettingsWindow(qt.QDialog):
    def __init__(self, parent):
        super(SettingsWindow, self).__init__(parent)

        self.setWindowTitle("Kanji Splitter")

        height = 200
        width = 400

        self.setMinimumHeight(height)
        self.setMinimumWidth(width)

        self.resize(width, height)

        self.setLayout(self.load_ui())

    def load_ui(self):
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

        dd_deck = deckDropdownLayout.dropdown

        dd_deck.addItem("None", 0)

        currentDeck = "None"

        for foundDeck in decks:
            if foundDeck.id == data["deck_id"]:
                currentDeck = foundDeck.name
            dd_deck.addItem(foundDeck.name, foundDeck.id)

        if currentDeck:
            dd_deck.setCurrentText(currentDeck)
        else:
            dd_deck.setCurrentIndex(0)

        layout.addLayout(deckDropdownLayout)

        # Scan deck
        b_scan = ButtonLabel(
                "Scan deck", 
                "Scan", 
                "This will scan the deck for kanji and add new cards for any found kanji/primitives. If cards already exist, that kanji/primitive will be skipped."
        )
        
        def scan():
            added = deck.scan_deck()
            MessageBox("", f"Done. {added} notes scanned.").exec()
        
        b_scan.button.clicked.connect(scan)

        layout.addLayout(b_scan)

        # Clear deck
        b_clear = ButtonLabel(
                "Clear deck", 
                "Clear", 
                "This will delete any cards created by this plugin inside your deck. (this will not delete the original cards)"
        )
        
        def clear():
            response = ConfirmationBox("Are you sure you wish to delete all Kanji Splitter cards from your deck? This action cannot be undone.").exec()

            if response == qt.QMessageBox.StandardButton.Yes:
                removed = deck.clear_deck()
                MessageBox("", f"Done. {removed} cards removed.").exec()
        
        b_clear.button.clicked.connect(clear)

        layout.addLayout(b_clear)

        # Note Options
        layout.addWidget(H3("Note options"))
        layout.addWidget(P("Changing these will not delete existing notes."))

        noteLayout = qt.QHBoxLayout()

        # Checkboxes Front Layout
        checkBoxFront = qt.QVBoxLayout()
        checkBoxFront.addWidget(Bold("Front"))

        # Checkboxes Back Layout
        checkBoxBack = qt.QVBoxLayout()
        checkBoxBack.addWidget(Bold("Back"))
        
        noteLayout.addLayout(checkBoxFront)
        noteLayout.addLayout(checkBoxBack)
        layout.addLayout(noteLayout)

        # Create Checkboxes
        checkBoxes = {}

        def createCheckBox(layout, key, label):
            cb_new = CheckBoxLabel(label)
            cb_new.setChecked(data[key])

            checkBoxes[key] = cb_new
            layout.addLayout(cb_new)

        createCheckBox(checkBoxFront, "show_front_keyword", "Show keyword")
        createCheckBox(checkBoxFront, "show_front_kanji", "Show kanji")
        createCheckBox(checkBoxFront, "show_drawing_canvas", "Show drawing canvas")

        createCheckBox(checkBoxBack, "show_back_kanji", "Show kanji")
        createCheckBox(checkBoxBack, "show_back_keyword", "Show keyword")
        createCheckBox(checkBoxBack, "show_edit_buttons", "Show edit buttons")
        createCheckBox(checkBoxBack, "show_kanji_strokes", "Show kanji strokes")
        createCheckBox(checkBoxBack, "show_dictionary_links", "Show dictionary links")

        checkBoxFront.addStretch()
        checkBoxBack.addStretch()

        layout.addWidget(Br())

        # Save / Cancel buttons
        layout.addStretch()
        buttonsLayout = qt.QHBoxLayout()
        buttonsLayout.addStretch()
        layout.addLayout(buttonsLayout)

        b_save = Button("Save")
        b_cancel = Button("Cancel")

        buttonsLayout.addWidget(b_save)
        buttonsLayout.addWidget(b_cancel)

        def save_action():
            data["deck_id"] = dd_deck.currentData()

            for key, checkBox in checkBoxes.items():
                checked = checkBox.isChecked()

                if checked != data[key]:
                    data[key] = checked

            config.update_config(data)
            model.create_model()
            self.close()
            
        def close_action():
            unsavedChanges = False

            for key, checkBox in checkBoxes.items():
                checked = checkBox.isChecked()

                if checked != data[key]:
                    unsavedChanges = True

            if unsavedChanges:
                response = ConfirmationBox("You have unsaved changes. Are you sure you wish to proceed?").exec()

                if response == qt.QMessageBox.StandardButton.Yes:
                    self.close()
            
        b_save.clicked.connect(save_action)
        b_cancel.clicked.connect(close_action)
        
        b_save.setFocusPolicy(qt.Qt.FocusPolicy.ClickFocus)

        return layout