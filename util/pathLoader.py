import os
import json
HOME_PATH = os.path.expanduser('~')
DATA_PATH = os.path.join(HOME_PATH, '.KJAppData')
CURRENT_PATH = os.getcwd()
DESKTOP_PET_DATA_PATH = os.path.join(DATA_PATH, 'DesktopPetConfig')
if not os.path.exists(DESKTOP_PET_DATA_PATH):
    os.makedirs(DESKTOP_PET_DATA_PATH)
    
CONF_PATH = os.path.join(DESKTOP_PET_DATA_PATH, 'conf.json')

def new_config_json():
    DATA_TEMPLATE = {
    "web": [
    ],
    "script": [
    ],
    "installPath": os.getcwd()
    }

    with open(CONF_PATH, 'w', encoding='utf-8') as f:
        json.dump(DATA_TEMPLATE, f)

    return DATA_PATH

def write_install_path(path):
    try:
        with open(CONF_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = new_config_json()
    data['installPath'] = path
    with open(CONF_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def get_install_path():
    try:
        with open(CONF_PATH, 'r', encoding='utf-8') as f:
            data =  json.load(f)['installPath']
    except:
        data = new_config_json()
    return data

    
def init_conf_path():
    print(os.getcwd())
    if not os.path.exists(CONF_PATH):
        new_config_json()
    else:
        if os.getcwd() == "C:\WINDOWS\System32" or os.getcwd == "C:\\WINDOWS\\system32":
            os.chdir(get_install_path())
        else:
            write_install_path(os.getcwd())
