import threading
import subprocess
import webbrowser
import os

def openExe(path):
    client_th = threading.Thread(target=subprocess.run, args=(path,))
    client_th.setDaemon(True)
    client_th.start()


def openUrl(url):
    client_th = threading.Thread(target=webbrowser.open, args=(url,))
    client_th.setDaemon(True)
    client_th.start()

def openFolder(path):
    if os.path.exists(path):
        os.startfile(path)
