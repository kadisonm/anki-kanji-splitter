from aqt import mw, gui_hooks
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from . import config
from .settings import SettingsWindow
from anki.notes import Note
from .kanji import scan_note
from .model import create_model, get_model

def start():
    debug = True

    config.load_config()

    window = SettingsWindow(mw)

    # Add config tool
    action = QAction("Kanji Splitter", mw)
    qconnect(action.triggered, window.open)
    mw.form.menuTools.addAction(action)

    # Add config action
    mw.addonManager.setConfigAction(__name__, window.open)

    def on_profile_loaded():
        create_model()

    gui_hooks.profile_did_open.append(on_profile_loaded)

    def addedNote(note: Note):  
        if not get_model():
            create_model()

        if note.has_tag("kanji-splitter"):
            return

        deckId = config.get_config()["deck_id"]

        result = mw.col.db.scalar(
            "SELECT 1 FROM cards WHERE nid = ? AND did = ?", note.id, deckId
        )

        if result:
            scan_note(note, deckId)
            
    gui_hooks.add_cards_did_add_note.append(addedNote)

    