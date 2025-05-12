from aqt import mw, gui_hooks
from aqt.utils import showInfo, qconnect
from anki.notes import Note
from anki.hooks_gen import note_will_be_addedz
import aqt.qt
import os

from . import config
from . import settings
from . import model
from . import deck
from . import editing

currentDir = os.path.dirname(os.path.abspath(__file__))
resourcesDir = os.path.join(currentDir, "resources")

iconsDir = os.path.join(resourcesDir, 'icons')
jpdbIconPath = os.path.join(iconsDir, 'jpdb_icon.png')
jishoIconPath = os.path.join(iconsDir, 'jisho_icon.png')

def start():
    # Load config
    config.load_config()

    def open_settings():
        window = settings.SettingsWindow()
        window.exec()

    def on_profile_loaded():
        # Create anki card model
        model.create_model()

        # Add settings tool button
        action = aqt.qt.QAction("Kanji Splitter", mw)
        qconnect(action.triggered, open_settings)
        mw.form.menuTools.addAction(action)

        # Add icons
        mw.col.media.addFile(jpdbIconPath)
        mw.col.media.addFile(jishoIconPath)

        # Add settings to addon page
        mw.addonManager.setConfigAction(__name__, open_settings)

    gui_hooks.profile_did_open.append(on_profile_loaded)

    # Listen for new notes in selected deck
    def addedNote(col, note, deckId):  
        if not model.get_model():
            model.create_model()

        if note.has_tag(deck.get_tag()):
            return
        
        chosenDeck = deck.get_deck()
        
        if chosenDeck:
            parentDeck = mw.col.decks.get(deckId)

            if parentDeck["name"] == chosenDeck["name"] or parentDeck["name"].startswith(chosenDeck["name"] + "::"):
                deck.scan_note(note)
            
    note_will_be_added.append(addedNote)

    # Listen for any cards being opened (to allow editing)
    def cardOpened(html: str, card, context):
        return editing.shouldModifyCard(html, card)

    gui_hooks.card_will_show.append(cardOpened)
    
    gui_hooks.webview_did_receive_js_message.append(editing.buttonClicked)

    