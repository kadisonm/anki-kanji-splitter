from anki.notes import Note
from aqt.utils import showInfo
from aqt import mw

from . import config
from . import model
from . import kanji

tagName = "kanji-splitter"

def get_tag():
    return tagName

def get_deck_id():
    return config.get_config()["deck_id"]

def get_deck():
    deckId = get_deck_id()
    deck = mw.col.decks.get(deckId)
    return deck

def create_note(newKanji):
    cardModel = model.get_model()
    note = Note(mw.col, cardModel)

    note["Kanji"] = newKanji

    note.add_tag(tagName)

    deckId = get_deck_id()
    mw.col.add_note(note, deckId)

    return note

def update_note(note): 
    noteKanji = note["Kanji"]

    keyword = kanji.get_heisig_keyword(noteKanji)

    if keyword:
        note["Keyword"] = keyword

    svg = kanji.get_svg(noteKanji)

    if svg:
        note["Strokes"] = svg

    mw.col.update_note(note)

def note_added(note: Note):
    deck = get_deck()
    deckId = get_deck_id()

    # Create new cards for each kanij
    originalCard = note.cards()[0]
    originalType = originalCard.type

    # Find new kanji
    foundKanji = kanji.get_kanji(note)

    newKanjiList = []

    for kanjiItem in foundKanji:
        if not mw.col.find_notes(f"Kanji:{kanjiItem} deck:{deck['name']} tag:{tagName}"):
            if kanjiItem not in newKanjiList:
                newKanjiList.append(kanjiItem)

    # Push due dates forward
    due = len(newKanjiList)

    originalCard.due += due
    mw.col.update_card(originalCard)

    mw.col.db.execute(
        "UPDATE cards SET due = due + ? WHERE did = ? AND due > ?",
        due, deckId, originalCard.due
    )

    # Add new cards
    for newKanji in newKanjiList:
        newNote = create_note(newKanji)
        update_note(newNote)

        newCard = newNote.cards()[0] 

        if originalType == 0:
            newCard.due = originalCard.due - due
        else:
            newCard.due = due

        mw.col.update_card(newCard)

        due -= 1

def scan_deck():
    deck = get_deck()

    cards = mw.col.find_cards(f"deck:{deck['name']} tag:{tagName}")

    for cardId in cards:
        card = mw.col.get_card(cardId)
        note = card.note()

        update_note(note)

def clear_deck():
    deck = get_deck()
    cards = mw.col.find_cards(f"deck:{deck['name']} tag:{tagName}")
    mw.col.remove_notes_by_card(cards)
