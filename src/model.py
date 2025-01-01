from aqt.utils import showInfo
from aqt import mw
import os
import json

modelName = "Kanji Splitter"

fieldsPath = os.path.join(os.path.dirname(__file__), "resources", "model", "fields.json")
frontHTMLPath = os.path.join(os.path.dirname(__file__), "resources", "model", "front_template.html")
backHTMLPath = os.path.join(os.path.dirname(__file__), "resources", "model", "back_template.html")
cssPath = os.path.join(os.path.dirname(__file__), "resources", "model", "styles.css")

with open(fieldsPath, 'r', encoding='utf-8') as file:
    fields = json.load(file)
    
with open(frontHTMLPath, 'r', encoding='utf-8') as file:
    qfmt_content = file.read()
    
with open(backHTMLPath, 'r', encoding='utf-8') as file:
    afmt_content = file.read()

with open(cssPath, 'r', encoding='utf-8') as file:
    css_content = file.read()


templates = [{
    'name': "Card 1",
    'qfmt': f"<style>{css_content}</style>\n{qfmt_content}",
    'afmt': f"<style>{css_content}</style>\n{afmt_content}"
}]

def create_model():
    global modelName
    
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