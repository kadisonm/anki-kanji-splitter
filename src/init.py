from aqt import mw, gui_hooks
from aqt.utils import showInfo, qconnect
from anki.notes import Note
import aqt.qt

from . import config
from . import settings
from . import kanji
from . import model
from . import deck

def start():
    # Load config
    config.load_config()

    window = settings.SettingsWindow(mw)

    # Add settings tool
    action = aqt.qt.QAction("Kanji Splitter", mw)
    qconnect(action.triggered, window.open)
    mw.form.menuTools.addAction(action)

    # Add settings action
    mw.addonManager.setConfigAction(__name__, window.open)

    # Create anki card model
    def on_profile_loaded():
        model.create_model()

    gui_hooks.profile_did_open.append(on_profile_loaded)

    # Listen for new notes in selected deck
    def addedNote(note: Note):  
        if not model.get_model():
            model.create_model()

        if note.has_tag(deck.get_tag()):
            return

        deckId = config.get_config()["deck_id"]

        result = mw.col.db.scalar(
            "SELECT 1 FROM cards WHERE nid = ? AND did = ?", note.id, deckId
        )

        if result:
            kanji.scan_note(note, deckId)
            
    gui_hooks.add_cards_did_add_note.append(addedNote)

    