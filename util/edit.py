import json
import requests
import os

import win32api
import win32ui
import win32gui
import win32con
from PIL import Image
import re

def init_exe_icon(path):
    savePath = "./resourses/exeicon/"
    name = re.findall(r'[^\\/:*?"<>|\r\n]+$', path)[0].split('.')[0]+ '.png'
    savePath = savePath + name
    if os.path.exists(savePath):
        return savePath
    # path = path.replace("\\", "/")
    icoX = win32api.GetSystemMetrics(win32con.SM_CXICON)

    large, small = win32gui.ExtractIconEx(path, 0)
    win32gui.DestroyIcon(small[0])

    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, icoX, icoX)
    hdc = hdc.CreateCompatibleDC()

    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0,0), large[0])

    # hbmp.SaveBitmapFile(hdc, savePath + "None.bmp")
    # bmpinfo = dataBitMap.GetInfo()
    bmpstr = hbmp.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGBA',
        (32,32),
        bmpstr, 'raw', 'BGRA', 0, 1
    )
    img.save(savePath)
    return savePath

init_exe_icon("./script/decode.exe") #This is just a example file path.
def init_icon(url, name):
    path = './resourses/webicon'
    m_path = './resourses/webicon/star.png'
    file_path = os.path.join(path, name + '.ico')
    if os.path.exists(file_path):
        return 0, file_path
    try:
        response = requests.get(url, stream=True, timeout=(1, 3))  # stream=True必须写上
        print("request")
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



def addWebSite(title, url):
    if title == "" or url == "":
        return
    with open('conf.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    webSites = data['web']
    for i in webSites:
        if i['title'] == title:
            return
    webSites.append({
        "title": title,
        "url": url
    })
    with open('conf.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

def delWebSite(name):
    with open('conf.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    webSites = data['web']
    for i in webSites:
        if i['title'] == name:
            webSites.remove(i)
            with open('conf.json', 'w', encoding='utf-8') as f:
                json.dump(data, f)
            return 0
    return 1