# Anki Kanji Learner

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