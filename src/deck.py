from anki.notes import Note
from aqt.utils import showInfo
from aqt import mw

from . import config

tagName = "kanji-splitter"

def get_tag():
    return tagName

def get_deck():
    deckId = config.get_config()["deck_id"]
    deck = mw.col.decks.get(deckId)
    return deck



def clear_deck():
    deck = get_deck()
    cards = mw.col.find_cards(f"deck:{deck['name']} tag:{tagName}")
    mw.col.remove_notes_by_card(cards)
