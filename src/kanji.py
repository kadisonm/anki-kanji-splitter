import re
import os
from anki.notes import Note
from aqt.utils import showInfo
from aqt import mw

currentDir = os.path.dirname(os.path.abspath(__file__))
userFilesDir = os.path.join(currentDir, "..", "user_files")

radicals = os.path.join(userFilesDir, 'radicals') 
keywords = os.path.join(userFilesDir, 'keywords')

def get_heisig_keyword(kanji):
    with open(keywords, 'r', encoding='eucjp') as file:
        fileContent = file.read()
    
    pattern = rf"^{kanji}\t([^\n\r]+)"
    match = re.search(pattern, fileContent, re.MULTILINE)

    if match:
        return match.group(1)
    else:
        return
    
def get_radicals(kanji):
    with open(radicals, 'r', encoding='iso2022_jp') as file:
        fileContent = file.read()
 
    pattern = r'.*[' + re.escape(kanji) + r'].+:\s*(.*)'

    match = re.search(pattern, fileContent, re.MULTILINE)

    if match:
        showInfo(match.group(1))
        return match.group(1)
    else:
        return []

def get_model():
    model = mw.col.models.by_name("Basic")

    if not model:
        showWarning("Basic model not found. Please ensure you have a 'Basic' card type.")
        return

    return model

def get_kanji(note: Note):
    foundKanji = []

    def findAllComponents(character):
        radicals = []

        for radical in get_radicals(character):
            if radical not in foundKanji:
                radicals.append(radical)
                foundKanji.append(radical)

        return radicals

    expression = note["Expression"] if "Expression" in note else ""

    for kanji in re.findall(r'[\u4e00-\u9faf\u3400-\u4dbf]', expression):
        if kanji not in foundKanji:
            result = findAllComponents(kanji)

            while result:
                for radical in result:
                    result = findAllComponents(radical)
            
            foundKanji.append(kanji)
    
    return foundKanji

def create_note(kanji: str, deckId, model): 
    keyword = get_heisig_keyword(kanji)

    if not keyword:
        return

    if mw.col.find_notes(f'"Front:{keyword}"'):
        print(f"Duplicate found: {keyword}")
        return

    newNote = Note(mw.col, model)
    newNote["Front"] = keyword
    newNote["Back"] = kanji
    newNote.add_tag("kanji-learner")

    mw.col.add_note(newNote, deckId)

    return newNote

def scan_note(note: Note, deckId):
    model = get_model()
    foundKanji = get_kanji(note)

    # Create new cards for each kanij
    originalCard = note.cards()[0]
    originalType = originalCard.type
    originalDue = originalCard.due
    due = len(foundKanji)

    for kanji in foundKanji:
        keyword = get_heisig_keyword(kanji)

        newNote = create_note(kanji, deckId, model)

        if not newNote:
            continue

        newCard = newNote.cards()[0] 

        if originalType == 0:
            newCard.due = originalDue - due
        else:
            newCard.due = due

        mw.col.update_card(newCard)

        due -= 1