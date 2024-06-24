from gui.head_info import *


def normal_page(master, mode, hd, handle=None):
    def return_exit():
        mode.set("exit")
        handle()

    def return_report():
        mode.set("report")
        handle()

    def return_base_info():
        mode.set("base_info")
        handle()
    
    def return_warehouse():
        mode.set('warehouse')
        handle()

    def return_stock():
        mode.set("stock")
        handle()

    def return_sales():
        mode.set("sales")
        handle()

    bg = 'white'

    # Separator(master, orient='horizontal', bg='#9ca8b8').pack(fill='x', side='bottom')


    # 操作菜单
    menus = tk.Frame(master, bg=bg)
    left = 90
    right = 45
    bold_font = ('song ti', 16, 'bold')
    button_fg = '#ffc66d'
    button_bg = '#44615D'
    tk.Button(menus, text='基础信息管理', font=bold_font, height=2,width=25, bd=4, fg=button_fg,
                     activebackground='white', bg=button_bg, command=return_base_info)\
        .pack(side='top', padx=(left, right), pady=(140, 50))
    tk.Button(menus, text='库房管理', font=bold_font, height=2,width=25, bd=4, fg=button_fg,
                     activebackground='white', bg=button_bg, command=return_warehouse) \
        .pack(side='top', padx=(left, right), pady=(0, 50))
    tk.Button(menus, text='进货管理', font=bold_font, height=2,width=25, bd=4, fg=button_fg,
                     activebackground='white', bg=button_bg, command=return_stock) \
        .pack(side='top', padx=(left, right), pady=(0, 130))

    menus.pack(side='left', fill='both', expand=True)

    menus = tk.Frame(master, bg=bg)
    left = 45
    right = 90
    tk.Button(menus, text='销售管理', relief='raised', font=bold_font, height=2,width=25, bd=4, fg=button_fg,
                     activebackground='white', bg=button_bg, command=return_sales) \
        .pack(side='top', padx=(left, right), pady=(140, 50))
        
    tk.Button(menus, text='报表系统', font=bold_font, height=2,width=25, bd=4, fg=button_fg,
                     activebackground='white', bg=button_bg, command=return_report) \
        .pack(side='top', padx=(left, right), pady=(0, 50))

    tk.Button(menus, text='退出账户', font=bold_font, height=2, width=25, bd=4,
                     activebackground='gray', fg="#F6FDFE",bg='#AD0600', command=return_exit) \
                     .pack(side='top', padx=(left, right), pady=(0, 0))

    menus.pack(side='left', fill='both', expand=True)


