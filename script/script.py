import threading
import subprocess
import webbrowser

def screenshot():
        subprocess.run('./script/screenshot.exe')

def openUrl(url):
    webbrowser.open(url)

def baidu():
    client_th = threading.Thread(target=wenku_decode)
    client_th.setDaemon(True)
    client_th.start()

def wenku_decode():
    subprocess.run('./script/wenku.exe')

def decode():
    client_th = threading.Thread(target=operate)
    client_th.setDaemon(True)
    client_th.start()

def operate():
    # os.system('decode.exe')
    subprocess.run('./script/decode.exe')