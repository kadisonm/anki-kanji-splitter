import os

from aqt import mw, gui_hooks, qt, reviewer
from aqt.utils import qconnect

from anki import hooks_gen
from anki.notes import Note
from anki.cards import Card
from anki.decks import DeckId
from anki.collection import Collection

from . import config
from . import settings
from . import model
from . import deck
from . import editing

def start():
    # Load config
    config.load_config()

    def open_settings():
        window = settings.SettingsWindow()
        window.exec()

    def on_profile_loaded():
        # Create anki card model
        model.create_model()

        # Add settings tool button
        action = qt.QAction("Kanji Splitter", mw)
        qconnect(action.triggered, open_settings)
        mw.form.menuTools.addAction(action)

        # Add icons
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        mw.col.media.add_file(os.path.join(current_dir, "resources", "icons", "jpdb_icon.png"))
        mw.col.media.add_file(os.path.join(current_dir, "resources", "icons", "jisho_icon.png"))

        # Add settings to addon page
        mw.addonManager.setConfigAction(__name__, open_settings)

    gui_hooks.profile_did_open.append(on_profile_loaded)

    # For detecting when a new note is added to the deck through the Anki GUI
    def note_added(note: Note):  
        if not model.get_model():
            model.create_model()

        if note.has_tag(deck.TAG_NAME):
            return
        
        parent_deck_id = mw.col.db.scalar("SELECT did FROM cards WHERE nid = ?", note.id)
        parent_deck = mw.col.decks.get(parent_deck_id)

        if parent_deck:
            cards: list[Card] = note.cards()
 
            if len(cards) >= 1:
                deck.scan_cards([cards[0]], True)
            
    gui_hooks.add_cards_did_add_note.append(note_added)

    # For detecting cards being added through Yomitan.
    def internal_note_added(col: Collection, note: Note, deckId: DeckId):
        if note.has_tag(deck.TAG_NAME) or not note.has_tag("Yomitan"):
            return
        
        print("Note added by Yomitan")
        
        elapsed = 0
        timer = qt.QTimer()

        def timer_ended():
            nonlocal elapsed
            nonlocal note

            elapsed += 1

            if len(note.card_ids()) > 0:
                note_added(note)
                return

            if elapsed < 10:
                timer.singleShot(1000, timer_ended)

        timer.singleShot(1000, timer_ended)

    hooks_gen.note_will_be_added.append(internal_note_added)

    # Listen for any cards being opened (to allow editing)
    def card_opened(html: str, card, context):
        return editing.shouldModifyCard(html, card)

    gui_hooks.card_will_show.append(card_opened)
    
    # Listen for any fields being edited
    def js_message_received(handled: any, message: str, context: any) -> any:
        if not message.startswith('kanji_splitter:'):
            return handled
        
        message = message.removeprefix('kanji_splitter:')

        if message.startswith('edit_mnemonic:'):
            message = message.removeprefix('edit_mnemonic:')

            if isinstance(context, reviewer.Reviewer):
                editing.editMnemonic(context.card.note(), message)

            return handled

        if message.startswith('edit_keyword:'):
            message = message.removeprefix('edit_keyword:')

            if isinstance(context, reviewer.Reviewer):
                editing.editKeyword(context.card.note(), message)

            return handled

        return handled

    gui_hooks.webview_did_receive_js_message.append(js_message_received)

    