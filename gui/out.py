from datetime import datetime
import tkinter as tk
from tkinter import messagebox  # tkinter 弹窗
import tkinter.ttk as ttk
from gui.config import *

def out_page(master, func, hd):
    title = tk.Label(master, text='退房页面', font=('fangsong ti', 18, 'bold'), bg='white') \
        .pack(fill='x', side='top', pady=10)

    cust_id = tk.StringVar()
    name = tk.StringVar()
    id = tk.StringVar()
    tel = tk.StringVar()
    price = tk.StringVar()
    today = datetime.now()
    today = f'{today.year}-{today.month}-{today.day}'
    def find():
        try:
            res = hd.select_needCheckout(cust_id.get(), today)
            if len(res) == 0:
                tk.messagebox.showerror(message=f"没有找到需要退房的消息")
                return
        except Exception as e:
            tk.messagebox.showerror(message=f"查询失败{e}")
            return
        serial_num = res[0][0]
        id.set(res[0][1])
        name.set(res[0][2])
        tel.set(res[0][3])
        price.set(res[0][4])

        try:
            ret = hd.select_infos_by_serialnum(serial_num)
        except:
            messagebox.showerror(message='')
            return
        x = tree.get_children()
        for item in x:
            tree.delete(item)
        for i in range(len(ret)):
            tree.insert('', i, values=ret[i])
        infos.pack(fill='x', side='top')
        tree.pack(side='top', fill='x')


    def checkout():
        try:
            hd.update_Checkout(id.get(), today)
        except:
            messagebox.showerror(message="退房异常")
            return
        messagebox.showinfo(message="退房成功")
        infos.pack_forget()
        tree.pack_forget()


    def back():
        master.destroy()
        func()

    search_line = tk.Frame(master, bg='white')
    tk.Label(search_line, text='身份证号：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(search_line, textvariable=cust_id, width=25, bd=0, font=myFont, bg='lightsteelblue') \
        .pack(side='left', padx=(0, 5))
    tk.Button(search_line, text='查询', font=('song ti', 13), bd=2, command=find, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left',padx=10)
    tk.Button(search_line, text='返回', font=('song ti', 13), bg='#4ABD96',fg="#FFFFFF", bd=2, command=back, width=5)\
        .pack(side='right', padx=(0, 20))
    search_line.pack(fill='x', side='top', pady=5)

    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    infos = tk.Frame(master)
    nameLine = tk.Frame(infos)

    tk.Label(nameLine, text='客户姓名:', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(nameLine, state='readonly', textvariable=name, width=13, font=('song ti', 16), bd=1, relief='groove').pack(
        side='left',
        padx=10)
    nameLine.pack(fill='x', side='top', pady=(20, 10))

    idLine = tk.Frame(infos)
    tk.Label(idLine, text='身份证号:', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(idLine, textvariable=id, state='readonly', width=25, font=myFont, relief='groove').pack(side='left',                                                                                             padx=10)
    idLine.pack(side='top', fill='x', pady=10)

    telLine = tk.Frame(infos)
    tk.Label(telLine, text='联系方式:', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(telLine, textvariable=tel, state='readonly', width=13, font=myFont, relief='groove') \
        .pack(side='left', padx=10)
    telLine.pack(side='top', fill='x', pady=10)

    priceLine = tk.Frame(infos)
    tk.Label(priceLine, text='  总价格:', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Label(priceLine, textvariable=price, font=('song ti', 13, 'bold')).pack(side='left', padx=(10, 0))
    tk.Button(priceLine, text='确认退房', font=('song ti', 13), command=checkout, bd=1, fg="#F6FDFE",bg='#ED5252') \
        .pack(side='left', padx=(200, 30))
    priceLine.pack(side='top', fill='x', pady=10)

    tree = ttk.Treeview(master, show='headings', height=500)
    tree["columns"] = ("房间类型", "房间号", "房价", "顾客1", "姓名1", "性别1", "电话1", "顾客2", "姓名2", "性别2", "电话2")
    tree.column("房间类型", width=50, anchor='center')
    tree.column("房价", width=50, anchor="center")
    tree.column("顾客1", width=150, anchor='center')
    tree.column("姓名1", width=60, anchor='center')
    tree.column("性别1", width=25, anchor='center')
    tree.column("电话1", width=80, anchor='center')
    tree.column("顾客2", width=150, anchor='center')
    tree.column("姓名2", width=60, anchor='center')
    tree.column("性别2", width=25, anchor='center')
    tree.column("电话2", width=80, anchor='center')
    tree.column("房间号", width=50, anchor='center')
    tree.heading("房间类型", text="房间类型")
    tree.heading("房价", text='房间价格')
    tree.heading("顾客1", text="身份证号")
    tree.heading("姓名1", text="姓名")
    tree.heading("性别1", text='性别')
    tree.heading("电话1", text="电话")
    tree.heading("顾客2", text="身份证号")
    tree.heading("姓名2", text="姓名")
    tree.heading("性别2", text="性别")
    tree.heading("电话2", text="电话")
    tree.heading("房间号", text="房间号")
    infos.pack_forget()


    pass
