from . import config
from . import deck
from . import model

from aqt import mw, reviewer, editor

import aqt.qt as qt

keyEditButton = model.getTextContent("elements", "keyword_edit_button.html")
mnemEditButton = model.getTextContent("elements", "mnemonic_edit_button.html")

def buttonClicked(handled, message: str, context):
    if not isinstance(context, reviewer.Reviewer):
        return handled

    note = context.card.note()
    
    if message == "edit_keyword":
        text, ok = qt.QInputDialog.getText(mw, "Enter new keyword", "This action is irreversible.")

        if ok and text:
            note["Keyword"] = text
            note["Source"] = "Custom keyword"
            mw.col.update_note(note)
            
            if isinstance(context, reviewer.Reviewer):
                context.web.eval(f"""
                    document.getElementById("keyword").innerHTML = `{text}`;
                    document.getElementById("source").innerHTML = `Custom keyword`;
                """)
          
    if message == "edit_mnemonic":
        text, ok = qt.QInputDialog.getText(mw, "Enter new mnemonic", "This action is irreversible.")
        
        if ok and text:
            note["Mnemonic"] = text
            mw.col.update_note(note)

            if isinstance(context, reviewer.Reviewer):
                context.web.eval(f"""
                    document.getElementById("mnemonic").innerHTML = `{text}`;
                """)

    return handled

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