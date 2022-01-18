from pickle import TRUE
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, qApp, QMenu, QSystemTrayIcon, QTextBrowser
from PyQt5 import QtMultimedia
from PyQt5.QtCore import Qt, QTimer, QObject, pyqtSignal, QUrl
from PyQt5.QtGui import QMovie, QIcon, QCursor, QFont
import threading
import random
import subprocess
import threading
import time

class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    print = pyqtSignal(str)
    clear = pyqtSignal()


gs = MySignals()

def playMeow():
    file = QUrl.fromLocalFile('./resourses/meow.mp3') # 音频文件路径
    content = QtMultimedia.QMediaContent(file)
    player = QtMultimedia.QMediaPlayer()
    player.setMedia(content)
    player.setVolume(50.0)
    player.play()
    time.sleep(1) #设置延时等待音频播放结束

class root(QMainWindow):
    def __init__(self):
        super().__init__()
        self.petCostom = ['05', '06']
        self.petHello = ['01']
        self.petDrag = '08'
        self.isMouseEnter = False
        self.is_follow_mouse = True
        self.mouse_drag_pos = self.pos()
        self.petNum = random.randint(0, 2)
        self.setUI()
        self.setSignal()

    def setSignal(self):
        gs.print.connect(self.print)
        gs.clear.connect(self.clear)

    def print(self, text):
        self.labelMessage.append(str(text))
        self.labelMessage.ensureCursorVisible()
        self.labelMessage.setVisible(True)
        self.disappearAfterTime(5000)

    def clear(self):
        self.labelMessage.clear()
        self.labelMessage.setVisible(False)
        self.isMouseEnter = False
        self.labelMessage.setAlignment(Qt.AlignCenter)


    def setUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.resize(150, 200)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        # 创建label盛放pet

        # 初始化标签控件
        self.labelMessage = QTextBrowser(self)
        self.labelMessage.setVisible(False)
        # self.labelMessage.setText("sjadkasjdkljljdasjkasdkjadksjdkjsdjakdjaskddjaskdjl")
        self.labelMessage.setFont(QFont())
        self.labelMessage.resize(150, 50)
        self.labelMessage.move(0, 0)
        self.labelMessage.setAlignment(Qt.AlignCenter)
        self.labelMessage.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.labelMessage.setAutoFillBackground(True)
        self.labelMessage.setStyleSheet(
            "font-size:15px;color:white;background-color: rgba(25, 25, 25, 0.5);border:None")

        self.label = QLabel('', self)
        self.label.resize(100, 100)
        self.label.move(25, 50)

        # 使pet在label中显示出来
        self.randomPet()
        self.actionInit()
        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomPet)
        self.timer.start(10000)

        # 最小化到托盘
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(self.petShow)
        self.tray_icon_menu.addAction(self.Quit)
        self.tray_icon = QSystemTrayIcon(self)
        self.trayIcon = QIcon('./resourses/ico.png')
        self.tray_icon.setIcon(self.trayIcon)
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()
        self.show()

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)
        hideAction = cmenu.addAction(self.petHide)
        clearAction = cmenu.addAction(self.Clear)
        shotAction = cmenu.addAction(self.shot)
        decodeAction = cmenu.addAction(self.urlaction)
        wenkuAction = cmenu.addAction(self.library)
        quitAction = cmenu.addAction(self.Quit)
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
    
    def actionInit(self):
        # 退出功能的定义
        self.Quit = QAction('退出', self, triggered=qApp.quit)
        self.Quit_Icon = QIcon('./resourses/exit.png')
        self.Quit.setIcon(self.Quit_Icon)
        # 清空空功能定义
        self.Clear = QAction('清空', self, triggered=self.clear)
        self.Clear_Icon = QIcon('./resourses/clear.png')
        self.Clear.setIcon(self.Clear_Icon)
        # 截图功能的定义
        self.shot = QAction('截图', self, triggered=self.screenshot)
        self.Shot_Icon = QIcon('./resourses/screenshot.png')
        self.shot.setIcon(self.Shot_Icon)
        # Deocde
        self.urlaction = QAction('解析', self, triggered=self.decode)
        self.url_icon = QIcon('./resourses/decode.ico')
        self.urlaction.setIcon(self.url_icon)
        # 百度文库功能
        self.library = QAction('文库', self, triggered=self.baidu)
        self.lib_icon = QIcon('./resourses/wenku.ico')
        self.library.setIcon(self.lib_icon)
        # 隐藏
        self.petHide = QAction('隐藏', self, triggered=self.pHide)
        self.petHide_icon = QIcon('./resourses/hide.png')
        self.petHide.setIcon(self.petHide_icon)
        # 显示
        self.petShow = QAction('显示', self, triggered=self.pShow)
        self.petShow_icon = QIcon('./resourses/show.png')
        self.petShow.setIcon(self.petShow_icon)

    def pShow(self):
        self.setVisible(True)
    
    def baidu(self):
        client_th = threading.Thread(target=self.wenku_decode)
        client_th.setDaemon(True)
        client_th.start()

    def wenku_decode(self):
        subprocess.run('./script/wenku.exe')

    def decode(self):
        client_th = threading.Thread(target=self.operate)
        client_th.setDaemon(True)
        client_th.start()

    def operate(self):
        # os.system('decode.exe')
        subprocess.run('./script/decode.exe')

    def setPet(self, petMode):
        self.gif = QMovie('./pets/' + str(petMode) + '.gif')
        self.gif.setScaledSize(self.label.size())
        self.label.setMovie(self.gif)
        self.gif.start()
        self.label.update()

    def pHide(self):
        self.setVisible(False)
    
    def randomPet(self):
        self.petNum = random.randint(0, len(self.petCostom) - 1)
        self.setPet(self.petCostom[self.petNum])


    def screenshot(self):
        subprocess.run('./script/screenshot.exe')

    '''鼠标左键按下时, 宠物将和鼠标位置绑定'''

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setPet(self.petDrag)
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    '''鼠标移动, 则宠物也移动'''

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    '''鼠标释放时, 取消绑定'''

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setPet(self.petHello[random.randint(0, len(self.petHello) - 1)])
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseDoubleClickEvent(self, event):
        self.clear()

    def enterEvent(self, event):
        if not self.labelMessage.toPlainText() == "":
            self.isMouseEnter = True
            self.labelMessage.setVisible(True)
        self.setPet(self.petHello[random.randint(0, len(self.petHello) - 1)])

    def leaveEvent(self, event):
        if self.isMouseEnter:
            self.isMouseEnter = False
            self.disappearAfterTime(1200)
        self.setPet(self.petCostom[self.petNum])
    
    def disappearAfterTime(self, time):
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.setLabelMessageDisappear)
        self.timer2.start(time)

    def setLabelMessageDisappear(self):
        if not self.isMouseEnter:
            self.labelMessage.setVisible(False)

