from anki.notes import Note
from aqt.utils import showInfo
from aqt import mw
import model
import re
import os
import json

currentDir = os.path.dirname(os.path.abspath(__file__))
resourcesDir = os.path.join(currentDir, "resources")

radicalsPath = os.path.join(resourcesDir, 'radicals.json') 
keywordsPath = os.path.join(resourcesDir, 'keywords.json')
kanjiPath = os.path.join(resourcesDir, 'Kanji')

keywords = None
radicals = None

def get_heisig_keyword(kanji):
    global keywords

    if not keywords:
        with open(keywordsPath, 'r', encoding="utf-8") as file:
            keywords = json.load(file)
    
    if kanji in keywords:
        return str.lower(keywords[kanji])
    else:
        return None
    
def get_radicals(kanji):
    global radicals

    if not radicals:
        with open(radicalsPath, 'r', encoding="utf-8") as file:
            radicals = json.load(file)
    
    if kanji in radicals:
        result = radicals[kanji]
        result = result.split()

        if kanji in result:
            result.remove(kanji)

        return result
    else:
        return []

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
            
            if kanji not in foundKanji:
                foundKanji.append(kanji)
    
    return foundKanji

def load_kanji_svg(kanji):
    codePoint = ord(kanji)
    hexCode = format(codePoint, 'x').zfill(5).lower() 
    
    path = os.path.join(kanjiPath, f"{hexCode}.svg")

    if os.path.exists(path):
        with open(path, 'r') as file:
            svgContent = file.read()
           
            match = re.search(r'(<svg[^>]*>.*?</svg>)', svgContent, re.DOTALL)
            
            if match:
                return match.group(1)

def create_note(kanji: str, deckId, cardModel): 
    keyword = get_heisig_keyword(kanji)

    if not keyword:
        return

    newNote = Note(mw.col, cardModel)
    newNote["Keyword"] = keyword
    newNote["Kanji"] = kanji

    svg = load_kanji_svg(kanji)

    if svg:
        newNote["Svg"] = svg

    newNote.add_tag("kanji-splitter")

    mw.col.add_note(newNote, deckId)

    return newNote

def scan_note(note: Note, deckId):
    cardModel = model.get_model()

    if not cardModel:
        return

    foundKanji = get_kanji(note)

    # Create new cards for each kanij
    originalCard = note.cards()[0]
    originalType = originalCard.type

    newKanji = []

    # Remove already existing cards
    for kanji in foundKanji:
        if not mw.col.find_notes(f'"Kanji:{kanji}"'):
            if kanji not in newKanji:
                newKanji.append(kanji)
        
    due = len(newKanji)

    # Push due dates forward
    originalCard.due += due
    mw.col.update_card(originalCard)

    mw.col.db.execute(
        "UPDATE cards SET due = due + ? WHERE did = ? AND due > ?",
        due, deckId, originalCard.due
    )

    # Add new cards
    for kanji in newKanji:
        newNote = create_note(kanji, deckId, cardModel)

        if not newNote:
            continue

        newCard = newNote.cards()[0] 

        if originalType == 0:
            newCard.due = originalCard.due - due
        else:
            newCard.due = due

        mw.col.update_card(newCard)

        due -= 1