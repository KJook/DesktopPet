import os
import win32api
import win32ui
import win32gui
import win32con
from PIL import Image
import re


def init_exe_icon(path):
    path = path.replace("\\", "/")
    savePath = "./test/"
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


init_exe_icon('./script/decode.exe')
