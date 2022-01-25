import threading
import requests
from util.pathLoader import CONF_PATH
import re
import json
import os
import win32api
import win32ui
import win32gui
import win32con
from PIL import Image


def init_exe_icon(path):
    if not os.path.exists(path):
        return "./resourses/bitbug_favicon.ico"
    savePath = "./resourses/exeicon/"
    name = re.findall(r'[^\\/:*?"<>|\r\n]+$', path)[0].split('.')[0]
    if os.path.exists(savePath + name + '.png'):
        return savePath + name + '.png'
    try:
        large, small = win32gui.ExtractIconEx(path, 0)
        win32gui.DestroyIcon(small[0])
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
        hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), large[0])
        # hbmp.SaveBitmapFile(hdc, savePath + name + '.bmp')
        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGBA',
            (ico_x, ico_y),
            bmpstr, 'raw', 'BGRA', 0, 1
        )
        img.save(savePath + name + '.png')
        return savePath + name + '.png'
    except:
        return './resourses/star.png'


def download_icon(url, file_path):
    try:
        response = requests.get(
            url, stream=True)  # stream=True必须写上
    except:
        return -1
    chunk_size = 1024  # 每次下载的数据大小
    try:
        if response.status_code == 200:  # 判断是否响应成功
            with open(file_path, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
            return 0
        else:
            return 2
    except Exception as e:
        return 1


def init_icon(url, name):
    path = './resourses/webicon'
    m_path = './resourses/star.png'
    file_path = os.path.join(path, name + '.ico')
    if os.path.exists(file_path):
        return 0, file_path
    else:
        t = threading.Thread(target=download_icon, args=(url, file_path))
        t.setDaemon(True)
        t.start()
        return 1, m_path
    


def addWebSite(title, url, attr, gs):
    if title == "" or url == "":
        return 3
    with open(CONF_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    webSites = data[attr]
    for i in webSites:
        if i['title'] == title:
            return 1
    webSites.append({
        "title": title,
        "url": url
    })
    with open(CONF_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    gs.refresh_conf.emit()
    return 0


def delWebSite(name, attr, gs):
    with open(CONF_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        webSites = data[attr]
    for i in webSites:
        if i['title'] == name:
            webSites.remove(i)
            with open(CONF_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f)
            gs.refresh_conf.emit()
            return 0
    return 1
