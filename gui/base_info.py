from gui.head_info import *


def base_info(master, mode, hd, handle=None):
    def getin_medicine():
        mode.set("medicine")
        handle()

    def getin_employee():
        mode.set("employee")
        handle()

    def getin_customer():
        mode.set("customer")
        handle()

    def getin_applier():
        mode.set("applier")
        handle()
    def return_normal():
        mode.set('normal')
        handle()

    bg = '#F0F0F0'

    # Separator(master, orient='horizontal', bg='#9ca8b8').pack(fill='x', side='bottom')


    # 操作菜单
    menus = tk.Frame(master, bg=bg)
    left = 90
    right = 45
    bold_font = ('song ti', 16)
    button_fg = '#ffc66d'
    button_bg = '#44615D'
    btn0 = tk.Button(menus, text='药品信息', font=bold_font, height=2,width=25, bd=3, fg=button_fg,
                      bg=button_bg, command=getin_medicine,)\
        .pack(side='top', padx=(left, right), pady=(170, 30))
    btn1 = tk.Button(menus, text='员工信息', font=bold_font, height=2,width=25, bd=3, fg=button_fg,
                     activebackground='white', bg=button_bg, command=getin_employee) \
        .pack(side='top', padx=(left, right), pady=(0, 30))
    

    menus.pack(side='left', fill='y', expand=True)


    menus = tk.Frame(master, bg=bg)
    left = 45
    right = 90
    btn0 = tk.Button(menus, text='供应商信息', font=bold_font, height=2,width=25, bd=3, fg=button_fg,
                     activebackground='white', bg=button_bg, command=getin_applier) \
        .pack(side='top', padx=(left, right), pady=(170, 30))
    btn1 = tk.Button(menus, text='客户信息', font=bold_font, height=2,width=25, bd=3, fg=button_fg,
                     activebackground='white', bg=button_bg, command=getin_customer) \
        .pack(side='top', padx=(left, right), pady=(0, 130))
    btn2 = tk.Button(menus, text='返回', font=bold_font, height=2,width=25, bd=3, fg=button_fg,
                     activebackground='white', bg='#ad0600', command=return_normal) \
        .pack(side='top', padx=(left, right), pady=(0, 0))
    menus.pack(side='left', fill='y', expand=True)



if __name__ == '__main__':
    window = tk.Tk()

