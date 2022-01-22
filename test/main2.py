
import os

from cachetools import FIFOCache

path = "E:\\OneDrive\\Script\\Waifu2x-Extension-GUI-Start_启动.bat"
path2 = "E:\\OneDrive\\图片\\二次元\\自动爬虫机器\\bilibiliSpider.exe"

fileName = os.path.basename(path2)
fileFolder = os.path.dirname(path2)
print(fileFolder)



x = os.popen('cd ' + fileFolder)
print(x.read())
fileName = fileName.replace(".exe", "")

os.system('.\\%s'%fileName)
