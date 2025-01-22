from anki.notes import Note
from aqt.utils import showInfo
from aqt import mw

from . import config

tagName = "kanji-splitter"

def get_tag():
    return tagName

def clear_deck():
    deckId = config.get_config()["deck_id"]
    deck = mw.col.decks.get(deckId)

    deckName = deck['name']

    cards = mw.col.find_cards(f"deck:{deckName} tag:{tagName}")
    
    mw.col.remove_notes_by_card(cards)
