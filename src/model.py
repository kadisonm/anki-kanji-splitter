from aqt.utils import showInfo
from aqt import mw
import os
import json
from . import config

modelName = "Kanji Splitter"

def getJSONContent(*paths):
    path = os.path.join(os.path.dirname(__file__), "resources", "model", *paths)

    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

def getTextContent(*paths):
    path = os.path.join(os.path.dirname(__file__), "resources", "model", *paths)

    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

fields = getJSONContent("fields.json")
front = getTextContent("front_template.html")
back = getTextContent("back_template.html")
css = getTextContent("styles.css")
warning = getTextContent("elements", "warning.html")

# Toggleable Elements
keyword = getTextContent("elements", "keyword.html")
kanji = getTextContent("elements", "kanji.html")
canvas = getTextContent("elements", "canvas.html")
canvasPreview = getTextContent("elements", "canvas_preview.html")
strokes = getTextContent("elements", "strokes.html")
composedOf = getTextContent("elements", "composed_of.html")
dictionaryLinks = getTextContent("elements", "dictionary_links.html")

def create_model():
    global modelName

    # Create card template based on model
    templates = [{
        'name': "Card 1",
        'qfmt': f"{warning}<style>{css}</style>\n{front}\n",
        'afmt': f"{warning}<style>{css}</style>\n{back}\n"
    }]

    data = config.get_config()

    if data["show_front_keyword"]:
        templates[0]['qfmt'] += f"\n{keyword}"

    if data["show_front_keyword"] & data["show_front_kanji"]:
        templates[0]['qfmt'] += "<hr>"
    
    if data["show_front_kanji"]:
        templates[0]['qfmt'] += f"\n{kanji}"
    
    if data["show_back_kanji"]:
        templates[0]['afmt'] += f"\n{kanji}"

    if data["show_back_keyword"]:
        templates[0]['afmt'] += f"\n{keyword}"

    if data["show_drawing_canvas"]:
        templates[0]['qfmt'] += f"\n{canvas}"
        templates[0]['afmt'] += f"\n{canvasPreview}"

    if data["show_kanji_strokes"]:
        templates[0]['afmt'] += f"\n{strokes}"

    if data["show_composed_of"]:
        templates[0]['afmt'] += f"\n{composedOf}"

    if data["show_dictionary_links"]:
        templates[0]['afmt'] += f"\n{dictionaryLinks}"
    
    mm = mw.col.models

    existingModel = mm.by_name(modelName)

    if existingModel:
        existingFields = {field['name']: field for field in existingModel['flds']}

        # Add missing fields
        for fieldName in fields:
            if fieldName not in existingFields:
                mm.add_field(existingModel, mm.new_field(fieldName))

        # Remove obselete fields
        for field in existingModel['flds']:
            if field['name'] not in fields:
                mm.remove_field(existingModel, field)

        existingTemplates = {template['name']: template for template in existingModel['tmpls']}
        for template in templates:
            # Add missing templates
            if template['name'] not in existingTemplates:
                newTemplate = mm.new_template(template['name'])
                newTemplate['qfmt'] = template['qfmt']
                newTemplate['afmt'] = template['afmt']
                mm.add_template(existingModel, newTemplate)
            else: # Update existing templates
                existingTemplate = existingTemplates[template['name']]
                if existingTemplate['qfmt'] != template['qfmt']:
                    existingTemplate['qfmt'] = template['qfmt']
                if existingTemplate['afmt'] != template['afmt']:
                    existingTemplate['afmt'] = template['afmt']
    else:
        existingModel = mm.new(modelName)

        for fieldName in fields:
            mm.add_field(existingModel, mm.new_field(fieldName))

        for template in templates:
            newTemplate = mm.new_template(template['name'])
            newTemplate['qfmt'] = template['qfmt']
            newTemplate['afmt'] = template['afmt']
            mm.add_template(existingModel, newTemplate)

    # Save the updated model
    mm.save(existingModel)

def get_model():
    global modelName

    model = mw.col.models.by_name(modelName)

    if not model:
        return

    return model