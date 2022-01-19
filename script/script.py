import threading
import subprocess
import webbrowser
def openExe(path):
    client_th = threading.Thread(target=subprocess.run, args=(path,))
    client_th.setDaemon(True)
    client_th.start()


def openUrl(url):
    client_th = threading.Thread(target=webbrowser.open, args=(url,))
    client_th.setDaemon(True)
    client_th.start()