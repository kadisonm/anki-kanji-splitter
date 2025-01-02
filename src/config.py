from aqt import mw

config = {
    'deck_id': 0,
    'front': {
        'showKanji': False,
        'showKeyword': False,
        'showDrawingPad': False,
    },
    'back': {}
}

def save_config() -> None:
    print(config)
    mw.addonManager.writeConfig(__name__, config)

def load_config():
    global config

    foundConfig = mw.addonManager.getConfig(__name__)

    if foundConfig:
        config = foundConfig
    else:
        save_config()

def get_config() -> dict:
    return config 

def update_config(new_config: dict) -> None:
    global config
    config.update(new_config)
    save_config()