from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from .config import load_config

config = load_config()

def process_deck() -> None:
    showInfo("test")

# Add menu item
action = QAction("Generate Kanji Cards", mw)
qconnect(action.triggered, process_deck)
mw.form.menuTools.addAction(action)