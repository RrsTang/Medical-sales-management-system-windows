import tkinter.ttk as ttk
from gui.head_info import *
from gui.config import *
from sql_handler.handler import handler
from tkinter import messagebox


def cust_page(master, func, handle):
    title = tk.Label(master, text='客户信息查询系统', font=('fangsong ti', 18, 'bold'), bg='white')\
        .pack(fill='x', side='top', pady=10)
    Separator(master, orient='horizontal').pack(side='top', fill='x')
    tree_and_scrollbar = tk.Frame(master, bg='white')
    ys = ttk.Scrollbar(tree_and_scrollbar, orient='vertical')
    tree = ttk.Treeview(tree_and_scrollbar, show='headings', height=500, yscrollcommand=ys.set)
    ys['command'] = tree.yview
    tree["columns"] = ("身份证", "姓名", "性别",  "联系方式", "房间号", "房间类型", "消费金额", "入住时间", "退房时间")
    tree.column("身份证", width=120, anchor='center')
    tree.column("姓名", width=70, anchor='center')
    tree.column("性别", width=50, anchor='center')
    tree.column("入住时间", width=120, anchor='center')
    tree.column("退房时间", width=120, anchor='center')
    tree.column("房间号", width=60, anchor='center')
    tree.column("房间类型", width=70, anchor='center')
    tree.column("联系方式", width=100, anchor='center')
    tree.column("消费金额", width=70, anchor='center')

    tree.heading("身份证", text="身份证")
    tree.heading("姓名", text="姓名")
    tree.heading("性别", text='性别')
    tree.heading("联系方式", text="联系方式")
    tree.heading("入住时间", text="入住时间")
    tree.heading("退房时间", text="退房时间")
    tree.heading("房间号", text="房间号")
    tree.heading("房间类型", text="房间类型")
    tree.heading("消费金额", text="消费金额")

    cust_id = tk.StringVar()
    cust_name = tk.StringVar()

    def find_all():
        try:
            ret = handle.select_all_customer()
        except:
            messagebox.showerror(message='未找到相关信息')
            return
        if len(ret) == 0:
            messagebox.showerror(message='未找到相关信息')
            return

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        for i in range(len(ret)):
            tree.insert('', i, values=ret[i])

    def find_by_id(event=None):
        id = cust_id.get()
        try:
            ret = handle.select_customer_information_by_id(id)
        except:
            messagebox.showerror(message='未找到相关信息')
            return
        if len(ret) == 0:
            messagebox.showerror(message='未找到相关信息')
            return

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        for i in range(len(ret)):
            tree.insert('', i, values=ret[i])

    def find_by_name(event=None):
        name = cust_name.get()
        try:
            ret = handle.select_customer_information_by_name(name)
        except:
            messagebox.showerror(message='未找到相关信息')
            return
        if len(ret) == 0:
            messagebox.showerror(message='未找到相关信息')
            return

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        for i in range(len(ret)):
            tree.insert('', i, values=ret[i])

    def back():
        master.destroy()
        func()

    search_line = tk.Frame(master, bg='white')

    tk.Label(search_line, text='身份证号：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    identry = tk.Entry(search_line, textvariable=cust_id, width=25, bd=0, font=myFont, bg='lightsteelblue')
    identry.bind('<Return>', find_by_id)
    identry.pack(side='left', padx=(0, 15))
    tk.Button(search_line, text='查询', font=('song ti', 13), bd=2, command=find_by_id, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left',padx=(0, 15))
    search_line.pack(side='top', fill='x', pady=5)
    tk.Button(search_line, text='查询所有', font=('song ti', 13), bd=2, command=find_all, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left')
    search_line.pack(side='top', fill='x', pady=5)
    tk.Button(search_line, text='返回', font=('song ti', 13), bg='#4ABD96',fg="#FFFFFF", bd=2, command=back, width=5)\
        .pack(side='right', padx=(0, 20))
    search_line.pack(fill='x', side='top', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    search_line0 = tk.Frame(master, bg='white')
    tk.Label(search_line0, text='姓    名：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    identry = tk.Entry(search_line0, textvariable=cust_name, width=25, bd=0, font=myFont, bg='lightsteelblue')
    identry.bind('<Return>', find_by_name)
    identry.pack(side='left', padx=(0, 15))
    tk.Button(search_line0, text='查询', font=('song ti', 13), bd=2, command=find_by_name, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left',padx=(0, 20))
    search_line0.pack(fill='x', side='top', pady=5)

    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')
    tree.pack(side='left', fill='x', expand=1)
    ys.pack(side='right', fill='y', anchor='w')
    tree_and_scrollbar.pack(side='top', fill='x', expand=1)


if __name__ == '__main__':
    root = tk.Tk()