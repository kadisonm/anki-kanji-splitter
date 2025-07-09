# General
- Finish writing README features and installation instructions
- Write Anki add-on post
- Fix the awful CSS

# Settings
- Build a card editor that can allow sections to be dragged around and placed wherever the user would like
- Maybe check if settings can be built using html?

# Decks
- Remove option for watching sub decks - Complicates reviews too much (maybe, check if it work stil)
- Get having multiple cards working, make sure subnotes are added to the right card
- Create custom undo operations
- Use [background operation](https://addon-docs.ankiweb.net/background-ops.html) to improve the performance 
https://github.com/ankitects/anki/issues/2628
https://forums.ankiweb.net/t/add-on-porting-notes-for-anki-2-1-45/11212

# Kanji
- 竜 adds itself as a component. Make sure to check this
- Kanji components are being added from right to left. Check this

# Keywords
- Some keywords are out of date with JPDB due to the original list being old (maybe introduce a way for me to rescrape it for updates)
- Show keyword for each component in kanji's component list (might need to use JS api)

# Keyboard Shortcuts
- Fix keyboard shortcuts to actually use the range of the selection and not just replace all the words
- Add being able to use a shortcut to remove highlights
