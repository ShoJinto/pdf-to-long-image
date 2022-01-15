#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# Created by ShoJinto at 2022/1/12

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Style
from threading import Thread
from converting import convert_pdf_to_long_image


def select_pdf():
    _pdfname = filedialog.askopenfilename(filetype=[("PDF file", "*.pdf")])
    if _pdfname != '':
        pdfname.set(_pdfname)
    # else:
    #     pdfname.set(f"No file was selected.")


def save_to():
    pdf_name = pdfname.get()
    if not pdf_name:
        messagebox.showinfo('提示', '请选择PDF文件')
        return ''
    _imgname = filedialog.asksaveasfilename(filetype=[("IMAGE file", "*.jpg")])
    if _imgname != '':
        if not _imgname.endswith('jpg'):
            _imgname = f"{_imgname}.jpg"
        imgname.set(_imgname)
        img_name = imgname.get()
        xargs = (progressbar, pbar_txt, messagebox)
        Thread(target=convert_pdf_to_long_image, args=(pdf_name, img_name, xargs)).start()


# 生成exe资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


# 创建屏幕居中的窗体
def center_window(window, w, h):
    # 1. 获取屏幕 宽、高
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # 2. 计算 x,y 位置
    x = (ws / 2) - (w / 2)
    y = (hs / 3) - (h / 2)
    window.geometry(f'{w:d}x{h:d}+{int(x)}+{int(y)}')


window = tk.Tk()
pdfname = tk.StringVar()
imgname = tk.StringVar()
pbar_txt = tk.StringVar()

style = Style(window)

# 设置窗口图标、窗口title、设置背景图
try:
    window.iconbitmap('pdf-to-image.ico')
    bg_image = tk.PhotoImage(file='pdf-to-image.gif')
except tk.TclError:
    bg_image = tk.PhotoImage(file=resource_path('pdf-to-image.gif'))
    window.iconbitmap(resource_path('pdf-to-image.ico'))
window.title("PDF转长图工具")
tk.Label(window, image=bg_image).grid(row=0, column=0, columnspan=4, rowspan=2,
                                      sticky=tk.W + tk.E + tk.N + tk.S, pady=5)

# 设置窗体大小以及禁用最大化（禁止用户调整窗体大小）
# window.geometry("560x220")
center_window(window, 560, 200)
window.resizable(False, False)

# progress bar
tk.Label(window, text='Progress:').grid(row=4, column=0, sticky=tk.E, padx=5, pady=20)
progressbar = Progressbar(window, orient=tk.HORIZONTAL, length=100, mode='determinate')
progressbar.grid(row=4, column=1, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=20)
tk.Label(window, textvariable=pbar_txt).grid(row=4, column=3, sticky=tk.W, padx=5, pady=20)

# pdf文件选择
tk.Label(window, text='PDF文件路径:').grid(row=2, column=0, padx=5)
tk.Entry(window, textvariable=pdfname, state=tk.DISABLED, width=45).grid(row=2, column=1, padx=5)
tk.Button(window, text="文件选择", command=select_pdf).grid(row=2, column=2, padx=5)

# 触发转换
tk.Button(window, text="开始转换", command=save_to).grid(row=2, column=3, padx=5)

window.mainloop()
