import aqt.qt as qt
import aqt

from . import config
from .ui import *
from . import model
from . import deck

class SettingsWindow(SettingsDialog):
    def __init__(self):
        super(SettingsWindow, self).__init__("Kanji Splitter")

        self.checkboxes = {}
        self.dropdowns = {}

        self.data = config.get_config()

        self.deckChanged = False

        self.tabs.addTab(self.deck_tab(), "Deck")
        self.tabs.addTab(self.card_tab(), "Card")
        self.tabs.addTab(self.about_tab(), "About")

        self.heading.addLayout(Logo(200))

    def deck_tab(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout()
        widget.setLayout(layout)

        # Selecting Deck
        deckDropdownLayout = DropdownLabel(
            "Select deck",
            "Select a deck to automatically add kanji/primitive cards to whenever a new note is created. Cards will be placed before the new note."
        )

        deckDropdown = deckDropdownLayout.dropdown

        self.dropdowns["deck_id"] = deckDropdown

        deckDropdown.addItem("None", 0)

        currentDeck = "None"
        decks = aqt.mw.col.decks.all_names_and_ids()

        for foundDeck in decks:
            if foundDeck.id == self.data["deck_id"]:
                currentDeck = foundDeck.name
            deckDropdown.addItem(foundDeck.name, foundDeck.id)

        if currentDeck:
            deckDropdown.setCurrentText(currentDeck)
        else:
            deckDropdown.setCurrentIndex(0)

        def deck_changed():
            self.deckChanged = True

        deckDropdown.currentIndexChanged.connect(deck_changed)

        layout.addLayout(deckDropdownLayout)

        # Scan Deck
        scan = ButtonLabel(
                "Scan deck", 
                "Scan", 
                "This will scan the deck for kanji and add new cards for any found kanji/components. If cards already exist, that kanji/components will be skipped."
        )
        
        def scan_action():
            if self.deckChanged:
                MessageBox("Warning", "You have unsaved changes to your selected deck. Please save before trying to perform any actions on it.").exec()
            else:
                response = ConfirmationBox("Are you sure you wish to scan your deck and add new cards for each kanji found?\n\nPlease note:\n• This will scan all NEW cards within your deck (does not include cards from this add-on or learnt cards already in your deck).\n• Any kanji not previously in your deck will be added as new cards.\n• If you dislike the results, you can undo any changes this add-on makes with Ctrl-Z.").exec()

                if response == qt.QMessageBox.StandardButton.Yes:
                    added = deck.scan_deck()

                    if added == None:
                        MessageBox("Warning", f"Please select a deck and save first before attempting to perform any actions.").exec()
                    else:
                        MessageBox("", f"Done. {added} Kanji Splitter cards added.").exec()
        
        scan.button.clicked.connect(scan_action)

        layout.addLayout(scan)

        # Clear Deck
        clear = ButtonLabel(
                "Clear deck", 
                "Clear", 
                "This will delete any cards created by this plugin inside your deck. (This will not delete your original cards)"
        )
        
        def clear_action():
            if self.deckChanged:
                MessageBox("Warning", "You have unsaved changes to your selected deck. Please save before trying to perform any actions on it.").exec()
            else:
                response = ConfirmationBox("Are you sure you wish to delete all Kanji Splitter cards from your deck? This action cannot be undone.").exec()

                if response == qt.QMessageBox.StandardButton.Yes:
                    if (result := deck.clear_deck()) == None:
                        print(result)
                        MessageBox("Warning", f"Please select a deck and save first before attempting to perform any actions.").exec()
                    else:
                        MessageBox("", f"Done. {result} notes removed.").exec()
        
        clear.button.clicked.connect(clear_action)

        layout.addLayout(clear)

        layout.addStretch()

        return widget

    def card_tab(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout()
        widget.setLayout(layout)

        # Keyword Source
        keywordsBox = GroupBox("Keywords")
        layout.addWidget(keywordsBox)

        keywordsDropdownLayout = DropdownLabel(
            "Keyword source",
            "Select which source to use keywords from. (Changing this will not change existing cards)"
        )

        keywordsBox.layout.addLayout(keywordsDropdownLayout)

        keywordsDropdown= keywordsDropdownLayout.dropdown

        self.dropdowns["keyword_source"] = keywordsDropdown

        keywordsDropdown.addItem("jpdb", 0)
        keywordsDropdown.addItem("RTK", 1)

        keywordsDropdown.setCurrentIndex(self.data["keyword_source"])

        # Note Options
        noteLayout = qt.QHBoxLayout()

        frontBox = GroupBox("Front")
        backBox = GroupBox("Back")

        noteLayout.addWidget(frontBox)
        noteLayout.addWidget(backBox)

        layout.addLayout(noteLayout)

        # Checkboxes
        self.checkboxes = {}

        def createCheckBox(layout, key, label):
            newCheckbox = CheckBoxLabel(label)
            newCheckbox.setChecked(self.data[key])

            self.checkboxes[key] = newCheckbox
            layout.addLayout(newCheckbox)

        createCheckBox(keywordsBox.layout, "use_alternative_keyword", "Use alternative source when a keyword is missing")

        createCheckBox(frontBox.layout, "show_front_keyword", "Show keyword")
        createCheckBox(frontBox.layout, "show_front_keyword_source", "Show keyword source")
        createCheckBox(frontBox.layout, "show_front_kanji", "Show kanji")
        createCheckBox(frontBox.layout, "show_front_mnemonic", "Show mnemonic")
        createCheckBox(frontBox.layout, "show_drawing_canvas", "Show drawing canvas")

        createCheckBox(backBox.layout, "show_back_kanji", "Show kanji")
        createCheckBox(backBox.layout, "show_back_keyword", "Show keyword")
        createCheckBox(backBox.layout, "show_back_keyword_source", "Show keyword source")
        createCheckBox(backBox.layout, "show_back_mnemonic", "Show mnemonic")
        createCheckBox(backBox.layout, "show_edit_buttons", "Show edit buttons")
        createCheckBox(backBox.layout, "show_kanji_strokes", "Show kanji strokes")
        createCheckBox(backBox.layout, "show_components", "Show components")
        createCheckBox(backBox.layout, "show_dictionary_links", "Show dictionary links")
        
        # Disclaimer
        layout.addWidget(Italics("Changing these settings will not delete existing notes."))

        frontBox.layout.addStretch()
        backBox.layout.addStretch()

        return widget
    
    def about_tab(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout()
        widget.setLayout(layout)

        layout.addWidget(P("An add-on that breaks down kanji cards into their components and adds them to your deck. <br>", True))


        layout.addWidget(P("<a href='https://github.com/kadisonm/anki-kanji-splitter'>↗ Repository</a>", True))

        layout.addWidget(P("<a href='https://buymeacoffee.com/kadisonm'>♡ Support</a>", True))

        layout.addWidget(P("<a href='https://github.com/kadisonm/anki-kanji-splitter/issues'>✎ Found an issue?</a><br>", True))


        layout.addWidget(P("By Kadison McLellan", True))

        layout.addWidget(P("GPL-3.0", True))

        layout.addStretch()

        layout.setAlignment(qt.Qt.AlignmentFlag.AlignCenter)

        return widget

    def save_action(self):
        for key, checkBox in self.checkboxes.items():
            checked = checkBox.isChecked()

            if checked != self.data[key]:
                self.data[key] = checked

        for key, dropdown in self.dropdowns.items():
            result = dropdown.currentData()

            if result != self.data[key]:
                self.data[key] = result

        config.update_config(self.data)
        model.create_model()
        self.close()
        
    def close_action(self):
        unsavedChanges = False

        for key, checkBox in self.checkboxes.items():
            checked = checkBox.isChecked()

            if checked != self.data[key]:
                unsavedChanges = True

        for key, dropdown in self.dropdowns.items():
                result = dropdown.currentData()

                if result != self.data[key]:
                    unsavedChanges = True

        if unsavedChanges:
            response = ConfirmationBox("You have unsaved changes. Are you sure you wish to proceed?").exec()

            if response == qt.QMessageBox.StandardButton.Yes:
                self.close()
        else:
            self.close()