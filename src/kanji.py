from anki.notes import Note
import xml.etree.ElementTree as ET
import re
import os
import json

currentDir = os.path.dirname(os.path.abspath(__file__))
resourcesDir = os.path.join(currentDir, "resources")

keywordsPath = os.path.join(resourcesDir, 'keywords.json')
kanjiPath = os.path.join(resourcesDir, 'Kanji')

keywords = None

def get_keywords(kanji):
    global keywords

    if not keywords:
        with open(keywordsPath, 'r', encoding="utf-8") as file:
            keywords = json.load(file)
    
    if kanji in keywords:
        return keywords[kanji]
    else:
        return None
    
isKanji = re.compile(r'^[\u4e00-\u9faf]+$')

namespaces = {"kvg": "http://kanjivg.tagaini.net"}

def is_valid_kanji(kanji):
    if len(kanji) != 1 and not re.fullmatch(r'[\u4e00-\u9faf\u3400-\u4dbf]', kanji):
        print(f"{kanji} is not a valid kanji.")
        return False
    
    return True

def get_components(kanji):
    elements = []

    if not is_valid_kanji(kanji):
        print(f"Skipping non-Unicode or pseudo-kanji: {kanji}")
        return elements

    codePoint = ord(kanji)
    hexCode = format(codePoint, 'x').zfill(5).lower()
    path = os.path.join(kanjiPath, f"{hexCode}.svg")

    if not os.path.exists(path):
        return elements

    tree = ET.parse(path)
    root = tree.getroot()

    kvgNamespace = '{http://kanjivg.tagaini.net}'
    
    for elem in reversed(list(root.iter())):  # bottom-up
        kvgElement = elem.attrib.get(f'{kvgNamespace}element')

        if kvgElement and kvgElement not in elements and kvgElement != kanji and is_valid_kanji(kvgElement):
            elements.append(kvgElement)

    return elements
 
def get_svg(kanji):
    if not is_valid_kanji(kanji):
        print(f"Skipping non-Unicode or pseudo-kanji: {kanji}")
        return kanji
    
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

    expression = note["Expression"] if "Expression" in note else ""

    for kanji in re.findall(r'[\u4e00-\u9faf\u3400-\u4dbf]', expression):
        if kanji not in foundKanji and len(kanji) == 1:
            result = get_components(kanji)

            for component in result:
                if component not in foundKanji:
                    foundKanji.append(component)
                    
            if kanji not in foundKanji:
                foundKanji.append(kanji)
    
    return foundKanji