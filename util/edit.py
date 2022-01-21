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
    savePath = "./resourses/exeicon/"
    name = re.findall(r'[^\\/:*?"<>|\r\n]+$', path)[0].split('.')[0] + '.png'
    savePath = savePath + name
    if os.path.exists(savePath):
        return savePath

    icoX = win32api.GetSystemMetrics(win32con.SM_CXICON)
    large, small = win32gui.ExtractIconEx(path, 0)
    win32gui.DestroyIcon(small[0])
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, icoX, icoX)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), large[0])
    bmpstr = hbmp.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGBA',
        (32, 32),
        bmpstr, 'raw', 'BGRA', 0, 1
    )
    img.save(savePath)

    return savePath


def init_icon(url, name):
    path = './resourses/webicon'
    m_path = './resourses/webicon/star.png'
    file_path = os.path.join(path, name + '.ico')
    if os.path.exists(file_path):
        return 0, file_path
    try:
        response = requests.get(
            url, stream=True, timeout=(1, 10))  # stream=True必须写上
    except:
        return -1, m_path
    chunk_size = 1024  # 每次下载的数据大小
    try:
        if response.status_code == 200:  # 判断是否响应成功
            with open(file_path, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
            return 0, file_path
        else:
            return 2, m_path
    except Exception as e:
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
