from . import config
from . import deck
from . import model

from aqt import mw, reviewer, editor

import aqt.qt as qt

keyEditButton = model.getTextContent("elements", "keyword_edit_button.html")
mnemEditButton = model.getTextContent("elements", "mnemonic_edit_button.html")

def editKeyword(note, text: str):
    note["Keyword"] = text
    note["Source"] = "Custom keyword"
    mw.col.update_note(note)

def editMnemonic(note, text: str):
    note["Mnemonic"] = text
    mw.col.update_note(note)

def injectEditButtons(html: str):
     html = html.replace('<div class="edit-hidden" id="keyword"></div>', keyEditButton)
     html = html.replace('<div class="edit-hidden" id="mnemonic"></div>', mnemEditButton)
     return html

def shouldModifyCard(html: str, card):
    note = card.note()

    if note.has_tag(deck.get_tag()):
            data = config.get_config()

            if data["show_edit_buttons"]:
                html = injectEditButtons(html)

    return html