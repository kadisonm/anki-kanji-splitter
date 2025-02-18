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

    composedOf = kanji.get_components(noteKanji)
    composedString = ""

    for item in composedOf:
        composedString += f"<li>{item}</li>\n"

    note["ComposedOf"] = f"Composed of\n<ul>\n{composedString}</ul>" 

    keywordsData = kanji.get_keywords(noteKanji)

    originalSource = config.get_config()["keyword_source"]

    keyword = "missing"

    if keywordsData:
        keywordsData[0] = keywordsData["jpdbKeyword"]
        keywordsData[1] = keywordsData["heisigKeyword"]

        keyword = keywordsData[originalSource]

        # Use alternative source if missing
        if keyword == "missing" and config.get_config()["use_alternative_keyword"]:
            originalSource = 1 if originalSource == 0 else 0
            keyword = keywordsData[originalSource]

    if originalSource == 0:
        note["Source"] = "jpdb keyword"
    else:
        note["Source"] = "RTK keyword"

    note["Keyword"] = keyword

    svg = kanji.get_svg(noteKanji)

    if svg:
        note["Strokes"] = svg

    mw.col.update_note(note)

def scan_note(note: Note):
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

    cards = mw.col.find_cards(f"deck:{deck['name']}", True)

    notesAdded = 0

    reversedCards = reversed(cards)

    for cardId in reversedCards:
        card = mw.col.get_card(cardId)
        
        note = card.note()

        if note.has_tag(tagName):
            continue

        scan_note(note)

        notesAdded += 1

    return notesAdded

def clear_deck():
    deck = get_deck()
    cards = mw.col.find_cards(f"deck:{deck['name']} tag:{tagName}")
    mw.col.remove_notes_by_card(cards)
    return len(cards)