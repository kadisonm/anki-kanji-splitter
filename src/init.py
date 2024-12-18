from aqt import AnkiApp, mw, gui_hooks
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from .config import load_config
from .configWindow import ConfigWindow

def start():
    config = load_config()

    window = ConfigWindow(mw)

    # Add config tool
    action = QAction("Kanji Learning Settings", mw)
    qconnect(action.triggered, window.open)
    mw.form.menuTools.addAction(action)

    # Add config action
    mw.addonManager.setConfigAction(__name__, window.open)

    def addedNote(card):
        print("added")
        print(card)

    gui_hooks.add_cards_did_add_note.append(addedNote)