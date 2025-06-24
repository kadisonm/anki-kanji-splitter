from anki.notes import Note
from anki.consts import CARD_TYPE_NEW
from aqt import mw

from . import config
from . import model
from . import kanji

tagName = "kanji-splitter"

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
    subDeckIds = get_deck_and_subdeck_ids()

    cardIds = mw.col.find_cards(f"deck:{deck['name']}")



    cards = [mw.col.get_card(id) for id in cardIds]

    filtered_cards = filter(lambda c: c.type == CARD_TYPE_NEW, cards)
    sorted_cards = sorted(filtered_cards, key=lambda c: c.due)

    return sorted_cards;

def create_note(newKanji):
    originalCardModel = mw.col.conf["curModel"]

    cardModel = model.get_model()

    note = Note(mw.col, cardModel)
    note.tags = [tagName]
    note["Kanji"] = newKanji

    deckId = get_deck_id()
    mw.col.add_note(note, deckId)

    if originalCardModel: # To stop anki from switching the default model to Kanji Splitter
        dummyNote = Note(mw.col, originalCardModel)
        dummyNote.tags = [tagName]
        mw.col.add_note(dummyNote, deckId)
        mw.col.remove_notes([dummyNote.id])

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

def scan_note(note: Note):
    deck = get_deck()
    deckId = get_deck_id()
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

    # mw.col.sched.set_due_date(ids, "1")

    # Might actually be able to use schedule_cards_as_new for this. 
    # Create the new sub cards -> order it properly in an array -> schedule them as new with restore position (Does this work?)
    # Stop reordering the deck manually
    # Hopefully this solves a lot of problems

    # Add new cards
    for newKanji in newKanjiList:
        newNote = create_note(newKanji)
        update_note(newNote)

        newCard = newNote.cards()[0] 
        newCard.due = originalDue + newKanjiLength - due

        mw.col.update_card(newCard)

        due -= 1

def reorder_deck():
    deck = get_deck()

    subDeckIds = get_deck_and_subdeck_ids()
    placeholders = ",".join("?" for _ in subDeckIds)
    query = f"SELECT id FROM cards WHERE did IN ({placeholders}) AND queue = 0 ORDER BY due ASC"

    lowestDueId = mw.col.db.first(query, *subDeckIds)

    if lowestDueId == None:
        return

    lowestDue = mw.col.get_card(lowestDueId[0]).due

    cards = get_new_cards()

    for i, card in enumerate(cards):
        card.due = lowestDue + i
        mw.col.update_card(card)

    return

def scan_deck():
    reorder_deck()

    deck = get_deck()

    if deck == None:
        return None

    cards = get_new_cards()

    notesAdded = 0

    for card in cards:
        note = card.note()

        if note.has_tag(tagName) or card.type != 0:
            continue

        scan_note(note)

        notesAdded += 1

    return notesAdded

def clear_deck():
    deck = get_deck()

    if deck == None:
        return None
    
    cards = mw.col.find_cards(f"deck:\"{deck['name']}\" tag:{tagName}")
    mw.col.remove_notes_by_card(cards)

    reorder_deck()

    return len(cards)