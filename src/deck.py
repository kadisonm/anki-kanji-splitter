from typing import Optional
from aqt import QWidget, mw, dialogs
from aqt.operations import CollectionOp
from aqt.utils import tooltip

from anki.notes import Note, NoteId
from anki.consts import CARD_TYPE_NEW
from anki.collection import Collection, OpChanges, OpChangesWithCount

from . import config
from . import model
from . import kanji

tagName = "kanji-splitter"
custom_undo_entries = {}

def get_tag():
    return tagName

def get_deck_id():
    return config.get_config()["deck_id"]

def get_deck_and_subdeck_ids():
    parent = get_deck()
    parentId = get_deck_id()

    deckIds = [parentId]
    
    if parent:
        for deck in mw.col.decks.all_names_and_ids():
            if deck.name.startswith(parent["name"] + "::"):
                deckIds.append(deck.id)

    return deckIds

def get_deck():
    deckId = get_deck_id()

    if deckId != 0:
        deck = mw.col.decks.get(deckId)
        return deck
    
    return None

def get_new_cards():
    deck = get_deck()

    if deck is None: return None

    subDeckIds = get_deck_and_subdeck_ids()

    cardIds = mw.col.find_cards(f"deck:{deck['name']}")

    cards = [mw.col.get_card(id) for id in cardIds]

    filtered_cards = filter(lambda c: c.type == CARD_TYPE_NEW, cards)

    sorted_cards = sorted(filtered_cards, key=lambda c: c.due)

    return sorted_cards

def create_note(newKanji):
    cardModel = model.get_model()

    note = Note(mw.col, cardModel)
    note.tags = [tagName]
    note["Kanji"] = newKanji

    deckId = get_deck_id()
    mw.col.add_note(note, deckId)

    # Stop anki from switching to Kanji Splitter note type for Add Card Screen
    mw.col.set_config("curModel", note.mid)

    return note

def update_note(note): 
    noteKanji = note["Kanji"]

    composedOf = kanji.get_direct_components(noteKanji)
    
    for item in composedOf:
        note["Components"] += f"<li class='component-item'>{item}</li>"

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

def reorder_deck():
    cards = get_new_cards()
    card_ids = [card.id for card in cards]

    mw.col.sched.reposition_new_cards(card_ids, 1, 1, False, True)

    return

def scan_note(note: Note):
    deck = get_deck()
    if deck is None: return None

    subDeckIds = get_deck_and_subdeck_ids()

    # Create new cards for each kanij
    originalCard = note.cards()[0]
    originalDue = originalCard.due

    # Find new kanji
    foundKanji = kanji.get_kanji(note)

    newKanjiList = []

    for kanjiItem in foundKanji:
        potentialDupes = mw.col.find_notes(f'"{kanjiItem}" deck:"{deck["name"]}" tag:"{tagName}"')
        dupeFound = False

        for dupeId in potentialDupes:
            dupeNote = mw.col.get_note(dupeId)

            if dupeNote['Kanji'] == kanjiItem:
                dupeFound = True
                break

        if kanjiItem not in newKanjiList and not dupeFound:
            newKanjiList.append(kanjiItem)

    # Push all cards after the scanned note forward
    newKanjiLength = len(newKanjiList)
    due = newKanjiLength

    placeholders = ",".join("?" for _ in subDeckIds)
    query = f"UPDATE cards SET due = due + ? WHERE did IN ({placeholders}) AND due >= ?"

    mw.col.db.execute(query, due, *subDeckIds, originalDue)

    # Add new cards
    for newKanji in newKanjiList:
        newNote = create_note(newKanji)
        update_note(newNote)

        newCard = newNote.cards()[0] 
        newCard.due = originalDue + newKanjiLength - due

        mw.col.update_card(newCard)

        due -= 1

    # Only run the following is Kanji Splitter cards were added
    if len(newKanjiList) == 0:
        return
    
    reorder_deck()

    # Stop anki from switching to Kanji Splitter note type for Add Card Screen
    dummyNote = Note(mw.col, mw.col.models.get(note.mid))
    dummyNote.tags = [tagName]
    mw.col.add_note(dummyNote, get_deck_id())
    mw.col.remove_notes([dummyNote.id])
    
def scan_deck():
    reorder_deck()

    cards = get_new_cards()

    notesAdded = 0

    for card in cards:
        note = card.note()

        if note.has_tag(tagName):
            continue

        scan_note(note)

        notesAdded += 1

    return notesAdded

def clear_deck() -> Optional[int]:
    if not (deck := get_deck()):
        return None

    cards = mw.col.find_cards(f"deck:\"{deck['name']}\" tag:{tagName}")

    to_remove = len(cards)

    def op(col: Collection):
        entry = col.add_custom_undo_entry("Clear Deck")

        mw.col.remove_notes_by_card(cards)

        reorder_deck()

        return col.merge_undo_entries(entry)

    CollectionOp(mw, op).run_in_background()

    return to_remove
