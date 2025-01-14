<h1 align="center">
Kanji Splitter
</h1>

<h4 align="center">An <a href="https://apps.ankiweb.net/">Anki</a> add-on that breaks down kanji cards into their components and adds them to your deck. </h4>

---

This add-on is **not** an official Anki add-on and is licensed under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) license.

## Attribution
This add-on uses the [RADKFILE and KRADFILE](http://www.edrdg.org/krad/kradinf.html) dictionary files. These files are the property of the [Electronic Dictionary Research and Development Group](https://www.edrdg.org/), and are used in conformance with the Group's [licence](https://www.edrdg.org/edrdg/licence.html).

The Kanji stroke diagrams are sourced from KanjiVG data, which is licensed under the [Creative Commons Attribution-Share Alike 3.0](https://creativecommons.org/licenses/by-sa/3.0/) license. 

## Contribution
Development for Anki with VSCode is a bit tricky, so here are some contribution instructions. (Note: You can use Pycharm as well)

### Installation with VSCode
1. Install [Python 3.9](https://www.python.org/downloads/release/python-390/)
2. Install [Visual Studio Code](https://code.visualstudio.com/)
3. Install [Python VS Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
4. Install [Pylance VS Extension]()
5. Git clone this repository into your `%AppData%\Anki2\addons21` folder and open it in VSCode
6. VS Terminal -> `py -3.9 -m venv env`
7. Terminal -> `env/Scripts/activate`
8. (env) Terminal -> `pip install -r requirements.txt`
9. Command Palette (Cmd/Ctrl+Shift+P) -> Python Select Interpreter -> `Python 3.9.0 ('env': venv)`

### Developing
It is recommended that you navigate to your Anki installation and run the `anki-console.bat` to gain access to the console while developing.

## Show your support

If you want to support me you can do so [here](https://www.buymeacoffee.com/kadisonm), but please know that this is not an expectation and this add-on is completely free.

[<img src="https://github.com/kadisonm/obsidian-reference-generator/assets/134670047/826ead37-1265-42b1-b171-928d1e17035f" width="200">](https://www.buymeacoffee.com/kadisonm)

Thank you so much for using my add-on.
