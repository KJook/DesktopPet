import os
import json
from tkinter import CURRENT
HOME_PATH = os.path.expanduser('~')
DATA_PATH = os.path.join(HOME_PATH, '.KJAppData')
CURRENT_PATH = os.getcwd()
DESKTOP_PET_DATA_PATH = os.path.join(DATA_PATH, 'DesktopPetConfig')
if not os.path.exists(DESKTOP_PET_DATA_PATH):
    os.makedirs(DESKTOP_PET_DATA_PATH)
CONF_PATH = os.path.join(DESKTOP_PET_DATA_PATH, 'conf.json')
DATA_TEMPLATE = {
    "web": [
    ],
    "script": [
    ],
    "installPath": os.getcwd()
    }   

if not os.path.exists(CONF_PATH):
    with open(CONF_PATH, 'w', encoding='utf-8') as f:
        json.dump(DATA_TEMPLATE, f)
else:
    with open(CONF_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except:
            with open(CONF_PATH, 'w', encoding='utf-8') as f:
                json.dump(DATA_TEMPLATE, f)
                data = DATA_TEMPLATE
    if not os.getcwd() == "C:\Windows\System32" or os.getcwd == "C:\\WINDOWS\\system32":
        data['installPath'] = os.getcwd()
    with open(CONF_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f)