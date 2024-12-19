from aqt import mw, gui_hooks
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from .config import load_config, get_config, save_config
from .configWindow import ConfigWindow
from anki.notes import Note
from .kanji import scan_note, get_heisig_keyword, get_radicals

def start():
    load_config()

    window = ConfigWindow(mw)

    # Add config tool
    action = QAction("Kanji Learning Settings", mw)
    qconnect(action.triggered, window.open)
    mw.form.menuTools.addAction(action)

    # Add config action
    mw.addonManager.setConfigAction(__name__, window.open)

    def addedNote(note: Note):  
        if note.has_tag("kanji-learner"):
            return

        deckId = get_config()["deck_id"]

        result = mw.col.db.scalar(
            "SELECT 1 FROM cards WHERE nid = ? AND did = ?", note.id, deckId
        )

        if result:
            scan_note(note, deckId)
            
    gui_hooks.add_cards_did_add_note.append(addedNote)

    