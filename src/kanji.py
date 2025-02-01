from aqt.utils import showInfo
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
        print(keywords[kanji])
        return keywords[kanji]
    else:
        return None
    
isKanji = re.compile(r'^[\u4e00-\u9faf]+$')

namespaces = {"kvg": "http://kanjivg.tagaini.net"}

def get_components(kanji):
    codePoint = ord(kanji)
    hexCode = format(codePoint, 'x').zfill(5).lower()
    
    path = os.path.join(kanjiPath, f"{hexCode}.svg")

    components = []

    if os.path.exists(path):
        tree = ET.parse(path)
        root = tree.getroot()

        for child in root.findall(".//*[@kvg:element]", namespaces):
            element = child.attrib.get("{http://kanjivg.tagaini.net}element")
            print(element)
            if element and isKanji.match(element):
                components.append(element)

    return reversed(components)
    
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
        components = []

        for component in get_components(character):
            if component not in foundKanji:
                showInfo(component)
                components.append(component)
                foundKanji.append(component)

        return components

    expression = note["Expression"] if "Expression" in note else ""

    for kanji in re.findall(r'[\u4e00-\u9faf\u3400-\u4dbf]', expression):
        if kanji not in foundKanji:
            result = findAllComponents(kanji)

            while result:
                for components in result:
                    result = findAllComponents(components)
            
            if kanji not in foundKanji:
                foundKanji.append(kanji)
    
    return foundKanji