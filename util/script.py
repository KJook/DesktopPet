import threading
import webbrowser
import os
import win32api
    
def runExe(path):
    # fileName = os.path.basename(path)
    # fileFolder = os.path.dirname(path)
    # print(fi)
    # x = os.popen('cd ' + fileFolder)
    # print("-----------------")
    # print(x.read())
    # fileName = fileName.replace(".exe", "")
    # os.system('.\\%s'%fileName)
    win32api.ShellExecute(0, 'open', path, '', os.path.dirname(path), 1)

def openExe(path):
        client_th = threading.Thread(target=runExe, args=(path,))
        client_th.setDaemon(True)
        client_th.start()

def openUrl(url):
    client_th = threading.Thread(target=webbrowser.open, args=(url,))
    client_th.setDaemon(True)
    client_th.start()

def openFolder(path):
    if os.path.exists(path):
        os.startfile(path)
