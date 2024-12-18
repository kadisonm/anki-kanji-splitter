import re
import os

# Get the current script directory
currentDir = os.path.dirname(os.path.abspath(__file__))
userFilesDir = os.path.join(currentDir, "..", "user_files")

radicals = os.path.join(userFilesDir, 'radicals') 
keywords = os.path.join(userFilesDir, 'keywords')

def get_heisig_keyword(kanji):
    with open(keywords, 'r', encoding='euc-jp', errors='ignore') as file:
        file_content = file.read()
    
    pattern = rf"^{kanji}\t([^\n\r]+)"
    match = re.search(pattern, file_content, re.MULTILINE)

    if match:
        return match.group(1)
    else:
        return "Keyword not found"
    
def get_radicals(kanji):
    with open(radicals, 'r', encoding='euc-jp', errors='ignore') as file:
        file_content = file.read()
 
    pattern = r'.*[' + re.escape(kanji) + r'].+:\s*(.*)'

    match = re.search(pattern, file_content, re.MULTILINE)

    if match:
        return match.group(1)
    else:
        return "Radicals not found"
    
def get_kanji():
    print("yeh")

def create_kanji_cards():
    print("yeh")