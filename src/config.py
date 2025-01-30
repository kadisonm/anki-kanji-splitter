from aqt import mw

config = {
    'deck_id': 0,
    'keyword_source': 0, # 0 = jpdb, 1 = rtk
    'show_front_keyword': True,
    'show_back_keyword': True,
    'show_front_kanji': False,
    'show_back_kanji': True,
    'show_drawing_canvas': True,
    'show_edit_buttons': True,
    'show_kanji_strokes': True,
    'show_dictionary_links': True,
}

def save_config() -> None:
    mw.addonManager.writeConfig(__name__, config)

def load_config():
    global config

    foundConfig = mw.addonManager.getConfig(__name__)

    if foundConfig:
        for key, value in config.items():
            if key not in foundConfig:
                foundConfig[key] = value

        config = foundConfig
    else:
        save_config()

def get_config() -> dict:
    return config 

def update_config(new_config: dict) -> None:
    global config
    config.update(new_config)
    save_config()