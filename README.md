<h1 align="center">
Kanji Splitter
</h1>

<h4 align="center">An <a href="https://apps.ankiweb.net/">Anki</a> add-on that splits kanji found in your deck into its separate components.

---

This add-on is **not** an official Anki add-on.

## Attribution
This add-on uses the [RADKFILE and KRADFILE](http://www.edrdg.org/krad/kradinf.html) dictionary files. These files are the property of the [Electronic Dictionary Research and Development Group](https://www.edrdg.org/), and are used in conformance with the Group's [licence](https://www.edrdg.org/edrdg/licence.html).

The Kanji stroke diagrams are sourced from KanjiVG data, which is licensed under the [Creative Commons Attribution-Share Alike 3.0](https://creativecommons.org/licenses/by-sa/3.0/) license. 

## Contribution
Development for Anki with VSCode is a bit tricky, so here are some contribution instructions. (Note: You can use Pycharm as well)

### Installation with VSCode
1. Install [Python 3.9](https://www.python.org/downloads/release/python-390/)
2. Install [Visual Studio Code](https://code.visualstudio.com/)
3. Install [Python VS Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
4. Git clone this repository into your `%AppData%\Roaming\Anki2\addons21` folder and open it in VSCode
5. VS Terminal -> `py -3.9 -m venv env`
6. Terminal -> `env/Scripts/activate`
7. (env) Terminal -> `pip install -r requirements.txt`
8. Command Palette (Cmd/Ctrl+Shift+P) -> Python Select Interpreter -> `Python 3.9.0 ('env': venv)`

### Developing
It is recommended that you navigate to your Anki installation and run the `anki-console.bat` to gain access to the console while developing.

https://wwwjdic.org/krad/kradinf.html
http://aiki.info/kanji/
