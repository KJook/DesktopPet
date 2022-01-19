#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：mgboy time:2020/8/2

import win32api
import win32con, winreg, os, sys
from PyQt5.QtWidgets import QMessageBox
"""判断键是否存在"""


def Judge_Key(self, key_name=None,
              reg_root=win32con.HKEY_CURRENT_USER,  # 根节点
              reg_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"  # 键的路径
              ):
    """
	:param key_name: #  要查询的键名
	:param reg_root: # 根节点
		#win32con.HKEY_CURRENT_USER
		#win32con.HKEY_CLASSES_ROOT
		#win32con.HKEY_CURRENT_USER
		#win32con.HKEY_LOCAL_MACHINE
		#win32con.HKEY_USERS
		#win32con.HKEY_CURRENT_CONFIG
	:param reg_path: #  键的路径
	:return:feedback是（0/1/2/3：存在/不存在/权限不足/报错）
	"""
    abspath=os.path.abspath(sys.argv[0])
    reg_flags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
    try:
        key = winreg.OpenKey(reg_root, reg_path, 0, reg_flags)
        location, type = winreg.QueryValueEx(key, key_name)
        # print("键存在", "location（数据）:", location, "type:", type)
        feedback = 0
        if location != abspath:
            feedback = 1
            # print('键存在，但程序位置发生改变')
    except FileNotFoundError as e:
        # print("键不存在", e)
        feedback = 1
    except PermissionError as e:
        QMessageBox.critical(self, "错误", "权限不足")
        feedback = 2
    except:
        QMessageBox.critical(self, "错误", "出现错误 错误码0x01")
        feedback = 3
    return feedback


"""开机自启动"""


def AutoRun(self):
    flag = self.autoRun.isChecked()
    key_name='kj.DesktopPet'
    abspath=os.path.abspath(sys.argv[0])
    # 如果没有自定义路径，就用os.path.abspath(sys.argv[0])获取主程序的路径，如果主程序已经打包成exe格式，就相当于获取exe文件的路径
    judge_key = Judge_Key(self, reg_root=win32con.HKEY_CURRENT_USER,
                          reg_path=r"Software\Microsoft\Windows\CurrentVersion\Run",  # 键的路径
                          key_name=key_name)
    # 注册表项名
    KeyName = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)    
    if flag:
        # 异常处理
        try:
            if judge_key == 0:
                return
                # print("已经开启了，无需再开启")
            elif judge_key == 1:
                win32api.RegSetValueEx(key, key_name, 0, win32con.REG_SZ, abspath)
                win32api.RegCloseKey(key)
                # print('开机自启动添加成功！')
        except:
            QMessageBox.critical(self, "错误", "开机自启动添加失败")
    else:
        try:
            if judge_key == 0:
                win32api.RegDeleteValue(key, key_name)  # 删除值
                win32api.RegCloseKey(key)
                # print('成功删除键！')
            elif judge_key == 1:
                QMessageBox.critical(self, "错误", "找不到开机启动项")
            elif judge_key == 2:
                QMessageBox.critical(self, "错误", "权限不足")
            else:
                QMessageBox.critical(self, "错误", "出现错误 错误码0x02")
        except:
            QMessageBox.critical(self, "错误", "删除失败 错误码0x03")
