from . import config
from . import deck
from . import model

editButton = model.getTextContent("elements", "edit_button.html")

def injectEditButton(html: str):
     return html.replace('<div class="edit-hidden"></div>', editButton)

def shouldModifyCard(html: str, card):
    note = card.note()

    if note.has_tag(deck.get_tag()):
            data = config.get_config()

            if data["show_edit_buttons"]:
                html = injectEditButton(html)

    return html