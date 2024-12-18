from aqt import mw

config = {
    'deck': "None",
}

def save_config() -> None:
    mw.addonManager.writeConfig(__name__, config)

def load_config():
    global config

    foundConfig = mw.addonManager.getConfig(__name__)

    print(foundConfig)

    if foundConfig:
        config = foundConfig
    else:
        save_config()

