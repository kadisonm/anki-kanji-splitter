from typing import Optional

from aqt import mw
from aqt.operations import CollectionOp
from aqt.utils import tooltip

from anki.notes import Note, NoteId
from anki.cards import Card, CardId
from anki.decks import DeckId
from anki.consts import CARD_TYPE_NEW
from anki.collection import Collection, OpChanges, AddNoteRequest

from . import config
from . import model
from . import kanji

TAG_NAME = "kanji-splitter"

def get_deck_id() -> DeckId:
    return config.get_config()["deck_id"]

def get_deck():
    deck_id = get_deck_id()

    if deck_id != 0:
        deck = mw.col.decks.get(deck_id)
        return deck
    
    return None

def get_new_cards() -> list[Card]:
    if not (deck := get_deck()):
        return []

    card_ids = mw.col.find_cards(f"deck:{deck['name']}")

    cards = [mw.col.get_card(id) for id in card_ids]

    only_new_cards = filter(lambda c: c.type == CARD_TYPE_NEW, cards)

    only_new_cards_sorted = sorted(only_new_cards, key=lambda c: c.due)

    return only_new_cards_sorted

def reorder_new_cards():
    cards = get_new_cards()
    card_ids = [card.id for card in cards]

    lowest_due = cards[0].due

    mw.col.sched.reposition_new_cards(card_ids, lowest_due, 1, False, True)

    return

def create_note(new_kanji) -> Note:
    if not (model_id := model.get_model_id()):
        model_id = model.get_model_id()

    note = Note(mw.col, model_id)
    note.tags = [TAG_NAME]

    # Kanji
    note["Kanji"] = new_kanji

    # Components
    components = kanji.get_direct_components(new_kanji)

    for item in components:
        note["Components"] += f"<li class='component-item'>{item}</li>"

    # Keyword & Source
    preferred_source = config.get_config()["keyword_source"]

    keyword = "missing"

    if keywords_data := kanji.get_keywords(new_kanji):
        keywords_data[0] = keywords_data["jpdbKeyword"]
        keywords_data[1] = keywords_data["heisigKeyword"]

        keyword = keywords_data[preferred_source]

        # Use alternative source if missing
        if keyword == "missing" and config.get_config()["use_alternative_keyword"]:
            preferred_source = 1 if preferred_source == 0 else 0
            keyword = keywords_data[preferred_source]

    if preferred_source == 0:
        note["Source"] = "jpdb keyword"
    elif preferential_attachment == 1:
        note["Source"] = "RTK keyword"
    else:
        note["Source"] = "Custom keyword"

    note["Keyword"] = keyword

    # SVG Strokes
    if svg := kanji.get_svg(new_kanji):
        note["Strokes"] = svg

    return note

def scan_cards(cards: list[Card], show_tooltip: bool) -> Optional[int]:
    if not (deck := get_deck()):
        return 0
    
    current_model = mw.col.get_config("curModel", 1)

    new_cards_in_deck = get_new_cards()

    notes_to_create: list[tuple[Note, int]] = []
    cards_to_update: list[tuple[CardId, int]] = [(card.id, card.due) for card in new_cards_in_deck]

    # Scan each card
    for card in cards:
        note = card.note()

        if note.has_tag(TAG_NAME):
            continue

        # Find new Kanji
        found_kanji = kanji.get_kanji(note)

        new_kanji = []

        for kanji_item in found_kanji:
            potential_dupes = mw.col.find_notes(f'"{kanji_item}" deck:"{deck["name"]}" tag:"{TAG_NAME}"')
            dupe_found = False

            for dupe_id in potential_dupes:
                dupe_note = mw.col.get_note(dupe_id)

                if dupe_note['Kanji'] == kanji_item:
                    dupe_found = True
                    break

            if kanji_item not in new_kanji and not dupe_found:
                new_kanji.append(kanji_item)

        # Push all cards due after scanned by component amount
        card_due = card.due

        for (id, due) in cards_to_update:
            if id == card.id:
                card_due = due

        push_by = len(new_kanji)

        new_to_update = []

        for (id, due) in cards_to_update:
            if (due >= card_due):
                new_to_update.append((id, due + push_by))
            else:
                new_to_update.append((id, due))

        cards_to_update = new_to_update

        # Create note and new due for each component found
        for i, kanji_item in enumerate(new_kanji):
            new_note = create_note(kanji_item)

            notes_to_create.append((new_note, card_due + i))

    def op(col: Collection):
        nonlocal notes_to_create
        nonlocal cards_to_update

        entry = col.add_custom_undo_entry(f"Add {len(notes_to_create)} Kanji Splitter Notes")

        # Add new notes
        deck_id = get_deck_id()

        note_requests = [AddNoteRequest(n, deck_id) for (n, due) in notes_to_create]
        
        col.add_notes(note_requests)
        
        # Update new notes and existing cards
        to_update = []

        for (note, due) in notes_to_create:
            card = note.cards()[0]
            card.due = due
            card.odue = due

            to_update.append(card)

        for (card_id, due) in cards_to_update:
            card = col.get_card(card_id)
            card.due = due
            card.odue = due

            to_update.append(card)

        col.update_cards(to_update)

        # Stop anki from switching to Kanji Splitter note type for Add Card Screen
        nonlocal current_model
        col.set_config("curModel", current_model)

        dummyNote = Note(col, current_model)
        dummyNote.tags = [TAG_NAME]
        mw.col.add_note(dummyNote, deck_id)
        mw.col.remove_notes([dummyNote.id])

        # Reorder new notes to keep things clean in case
        reorder_new_cards()

        return col.merge_undo_entries(entry)
    
    added = len(notes_to_create)
    
    def success(out: OpChanges):
        if show_tooltip:
            message = f"<b>Added</b> {added} Kanji Splitter Notes"
            
            tooltip(message, parent=mw)

    if added > 0:
        CollectionOp(mw, op).success(success).run_in_background()
    
    return added

def scan_deck() -> Optional[int]:
    if not get_deck():
        return None
    
    cards = get_new_cards()

    return scan_cards(cards, False)

def clear_deck() -> Optional[int]:
    if not (deck := get_deck()):
        return None

    cards = mw.col.find_cards(f"deck:\"{deck['name']}\" tag:{TAG_NAME}")

    to_remove = len(cards)

    def op(col: Collection):
        entry = col.add_custom_undo_entry("Clear Deck")

        mw.col.remove_notes_by_card(cards)

        reorder_new_cards()

        return col.merge_undo_entries(entry)

    CollectionOp(mw, op).run_in_background()

    return to_remove
