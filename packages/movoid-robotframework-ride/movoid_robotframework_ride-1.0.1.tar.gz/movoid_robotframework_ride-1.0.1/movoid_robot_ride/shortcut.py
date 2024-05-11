#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : shortcut
# Author        : Sun YiFan-Movoid
# Time          : 2024/5/11 4:28
# Description   : 
"""
import sys
from tkinter import Tk, filedialog


def start_ride():
    tk = Tk()
    tk.withdraw()
    folder = filedialog.askdirectory(title='choose testcase please')
    if folder:
        from robotide import main
        sys.path.append(folder)
        main(folder)


def create_shortcut(name: str = 'Ride'):
    import platform
    ps = platform.system()
    if ps == 'Windows':
        create_shortcut_windows(name)
    else:
        print('linux and mac is under developed')


def create_shortcut_windows(name: str):
    import os
    import sys
    import pathlib
    try:
        from win32com.shell import shell, shellcon
    except ImportError:
        sys.stderr.write("Cannot create desktop shortcut.\nPlease install pywin32 from https://github.com/mhammond/pywin32 or pip install pywin32")
        return False
    desktop = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)
    link = pathlib.Path(desktop) / f'{name}.lnk'
    icon = pathlib.Path(sys.prefix) / 'Lib' / 'site-packages' / 'robotide' / 'widgets' / 'robot.ico'
    if link.exists():
        link.unlink()
    import pythoncom
    shortcut = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    command_args = " -c \"from movoid_robot_ride import start_ride; start_ride()\""
    shortcut.SetPath(sys.executable)
    shortcut.SetArguments(command_args)
    shortcut.SetDescription("Robot Framework testdata editor")
    shortcut.SetIconLocation(str(icon), 0)
    persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
    persist_file.Save(str(link), 0)


if __name__ == '__main__':
    create_shortcut(*sys.argv[1:])
