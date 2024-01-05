from datetime import datetime
import tkinter as tk
from gui.config import *
from tkinter.ttk import Separator


def head_handle(master, name:str):
    fg = '#ffc66d'
    bg = '#688A7E'
    titleFrame = tk.Frame(master, bg=bg)
    tk.Label(titleFrame, text='医药销售管理系统',  fg=fg ,bg=bg, font=('song ti', 30, 'bold')).pack(fill='x', side='top', pady=35)
    titleFrame.pack(side='top', fill='x')
