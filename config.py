from typing import Dict
from aqt import mw
from aqt.qt import *

config = {
    'deck': "0",
}

def save_config() -> None:
    mw.addonManager.writeConfig(__name__, config)

def load_config() -> Dict:
    global config

    foundConfig = mw.addonManager.getConfig(__name__)

    if foundConfig:
        config = foundConfig
    else:
        save_config()

    return config
