from anki.notes import Note
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

def get_keywords(kanji):
    global keywords

    if not keywords:
        with open(keywordsPath, 'r', encoding="utf-8") as file:
            keywords = json.load(file)
    
    if kanji in keywords:
        print(keywords[kanji])
        return keywords[kanji]
    else:
        return None
    
def get_components(kanji):
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
    
def get_svg(kanji):
    codePoint = ord(kanji)
    hexCode = format(codePoint, 'x').zfill(5).lower() 
    
    path = os.path.join(kanjiPath, f"{hexCode}.svg")

    if os.path.exists(path):
        with open(path, 'r') as file:
            svgContent = file.read()
           
            match = re.search(r'(<svg[^>]*>.*?</svg>)', svgContent, re.DOTALL)
            
            if match:
                return match.group(1)

def get_kanji(note: Note):
    foundKanji = []

    def findAllComponents(character):
        radicals = []

        for radical in get_components(character):
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