import tkinter as tk
from tkinter.ttk import Separator
from gui.config import *


def login_page(master, name, pwd, login_handle):
    titleFrame = tk.Frame(master, bg='#688A7E')

    tk.Label(titleFrame, text='医药销售管理系统', fg='#ffc66d' ,bg='#688A7E', font=('song ti', 30, 'bold')).pack(fill='x', side='top', pady=115)

    titleFrame.pack(side='top', fill='x')

    # 用户信息
    bg = 'White'
    infoFrame = tk.Frame(master, bg=bg)

    def focus_next(event=None):
        pwdEntry.focus_set()

    # 用户名框架
    usrFrame = tk.Frame(infoFrame, bg=bg)
    tk.Label(usrFrame, text="账户：", bg=bg,
             font=myFont).pack(side='left', padx=(220, 10))
    nameEntry = tk.Entry(usrFrame, show=None, width=25, textvariable=name, bd=0,
             font=myFont)
    nameEntry.bind('<Return>', focus_next)
    nameEntry.pack(side='left')
    usrFrame.pack(side='top', anchor='nw', pady=(100, 0))

    Separator(infoFrame, orient='horizontal').pack(padx=(300, 200), pady=(0, 20), fill='x')

    # 用户密码框架
    pwdFrame = tk.Frame(infoFrame, bg=bg)
    tk.Label(pwdFrame, text="密码：", bg=bg,
             font=myFont).pack(side='left', padx=(220, 10), pady=0)
    pwdEntry = tk.Entry(pwdFrame, show='●', width=25, textvariable=pwd, bd=0,
             font=myFont)
    pwdEntry.bind('<Return>', login_handle)
    pwdEntry.pack(side='left')
    pwdFrame.pack(side='top', anchor='nw')

    Separator(infoFrame, orient='horizontal').pack(padx=(300, 200), pady=(0, 20), fill='x')

    button_fg = '#cccccc'
    button_bg = '#44615D'
    btnFrame = tk.Frame(infoFrame, bg=bg)
    tk.Button(btnFrame, text='登录系统', relief=tk.RAISED, activebackground='white', font=myFont, width=31, height=1, fg=button_fg,
              bg=button_bg, command=login_handle, bd=4)\
                    .pack(side='left', padx=(350, 0), pady=(80,10))
    btnFrame.pack(side='top', anchor='nw')

    infoFrame.pack(fill='x')



