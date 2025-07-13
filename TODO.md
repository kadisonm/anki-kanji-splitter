# General
- Finish writing README features and installation instructions
- Write Anki add-on post
- Fix the awful CSS
- Refactor other scripts to have better types and styling
- Add a release and build script (look into this)
- Specify no network calls but explain how each kanji diagram is included within the plugin

# Tests
- Write them haha (actually really really need them)

# Settings
- Build a card editor that can allow sections to be dragged around and placed wherever the user would like
- Maybe check if settings can be built using html?

# Decks
- Drop support for sub decks
- Get having multiple cards working, make sure subnotes are added to the right card
- Refactor getting the notes to create and update just to be a bit more readable
- Check if Anki's findDupe function works

# Model
- Make sure that when getting the model, one is always returned (if not created yet)

# Kanji
- 竜 adds itself as a component. Make sure to check this
- Kanji components are being added from right to left. Check this

# Keywords
- Some keywords are out of date with JPDB due to the original list being old (maybe introduce a way for me to rescrape it for updates)
- Show keyword for each component in kanji's component list (might need to use JS api)

# Keyboard Shortcuts
- Fix keyboard shortcuts to actually use the range of the selection and not just replace all the words
- Add being able to use a shortcut to remove highlights
- Write documentation to this somewhere
