# Development
Development for Anki within VSCode can be a bit tricky, so here are some contribution instructions. (Note: You can use Pycharm as well)

## Installation with VSCode
1. Install [Python 3.9](https://www.python.org/downloads/release/python-390/)
2. Install [Visual Studio Code](https://code.visualstudio.com/)
3. Install [Python VS Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
4. Install [Pylance VS Extension]()
5. Git clone this repository into your `%AppData%\Anki2\addons21` folder and open it in VSCode
6. VS Terminal -> `py -3.9 -m venv env`
7. Terminal -> `env/Scripts/activate`
8. (env) Terminal -> `pip install -r requirements.txt`
9. Command Palette (Cmd/Ctrl+Shift+P) -> Python Select Interpreter -> `Python 3.9.0 ('env': venv)`

## Debugging with VSCode
It is recommended that you navigate to your Anki installation and run the `anki-console.bat` to gain access to the console while developing.

Creating a VSCode task to do this for you is extremely helpful, an example can be found below.

```json
{
    "version": "2.0.0",
    "tasks": [
      {
        "label": "Run Anki",
        "type": "shell",
        "command": "path\\to\\your\\Anki Install\\anki-console.bat",
      }
    ]
}
```