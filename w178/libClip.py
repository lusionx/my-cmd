# coding: utf-8

import ctypes
def get():
    ctypes.windll.user32.OpenClipboard(None)
    pcontents = ctypes.windll.user32.GetClipboardData(1) # 1 means CF_TEXT 
    data = ctypes.c_char_p(pcontents).value
    ctypes.windll.user32.CloseClipboard()
    return data
