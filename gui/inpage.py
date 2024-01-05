import tkinter as tk
from gui.config import *
import tkinter.ttk as ttk
from datetime import datetime
from tkinter import messagebox

def in_page(master, func, handle):
        
    def back():
        master.destroy()
        func()
        pass

    name = tk.StringVar()

    infos = tk.Frame(master)

    serial_num = ""

    tree = ttk.Treeview(master, show='headings', height=500)

    def find(event=None):
        infos.pack_forget()
        tree.pack_forget()
        date = datetime.now()
        try:
            ret = handle.select_customer_info_by_id_and_date(cust_id.get(), f'{date.year}-{date.month}-{date.day}')
        except:
            messagebox.showerror(message='身份证号格式错误，请重新输入')
            return
        if len(ret) == 0:
            messagebox.showerror(message='没有需要处理的预订信息')
            return
        nonlocal name
        nonlocal id
        nonlocal tel
        nonlocal serial_num
        nonlocal price
        serial_num = ret[0][0]
        id.set(ret[0][1])
        name.set(ret[0][2])
        tel.set(ret[0][3])
        try:
            price.set(handle.settle_account(serial_num))
            ret = handle.select_infos_by_serialnum(serial_num)
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

    def submit():
        infos.pack_forget()
        tree.pack_forget()
        date = datetime.now()
        try:
            handle.live_in(serial_num)
        except:
            messagebox.showerror(message='更新失败，请检查预订信息是否存在')
            return
        messagebox.showinfo(message='已完成入住办理')

    def delete():
        infos.pack_forget()
        tree.pack_forget()
        try:
            handle.delete_book_info_by_serial_num(serial_num)
        except:
            messagebox.showerror(message='更新失败，请检查预订信息是否存在')
            return
        messagebox.showinfo(message='成功删除预订信息')

    tk.Label(master, text='预订信息/入住办理', font=('fangsong ti', 18, 'bold'), bg='white').pack(fill='x', side='top', pady=10)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')
    search_line = tk.Frame(master, bg='white')
    cust_id = tk.StringVar()
    tk.Label(search_line, text='身份证号：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    identry = tk.Entry(search_line, textvariable=cust_id, width=25, bd=0, font=myFont, bg='lightsteelblue')
    identry.bind('<Return>', find)
    identry.pack(side='left', padx=(0, 5))
    tk.Button(search_line, text='查询', font=('song ti', 13), bd=2, command=find, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left',padx=15)
    tk.Button(search_line, text='返回', font=('song ti', 13), bg='#4ABD96',fg="#FFFFFF" , bd=2, command=back, width=5) \
        .pack(side='right', padx=(0, 20))
    search_line.pack(fill='x', side='top', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    nameLine = tk.Frame(infos)

    tk.Label(nameLine, text='客户姓名:', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(nameLine, state='readonly', textvariable=name, width=13, font=('song ti', 16), bd=1, relief='groove').pack(side='left',
                                                                                                 padx=10)
    nameLine.pack(fill='x', side='top', pady=(20, 10))

    idLine = tk.Frame(infos)
    id = tk.StringVar()
    tk.Label(idLine, text='身份证号:', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(idLine, textvariable=id, state='readonly', width=25, font=myFont, relief='groove').pack(side='left', padx=10)
    idLine.pack(side='top', fill='x', pady=10)

    telLine = tk.Frame(infos)
    tel = tk.StringVar()
    tk.Label(telLine, text='联系方式:', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(telLine, textvariable=tel, state='readonly', width=13, font=myFont, relief='groove')\
        .pack(side='left', padx=10)
    telLine.pack(side='top', fill='x', pady=10)

    priceLine = tk.Frame(infos)
    price = tk.StringVar()
    tk.Label(priceLine, text='  总价格:', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Label(priceLine, textvariable=price, font=('song ti', 13, 'bold')).pack(side='left', padx=(10, 0))
    tk.Button(priceLine, text='确认入住', font=('song ti', 13), command=submit, bd=1, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left', padx=(200, 30))
    tk.Button(priceLine, text='删除预订信息', font=('song ti', 13), command=delete, bd=1, fg="#F6FDFE",bg='#ED5252') \
        .pack(side='left', padx=30)
    priceLine.pack(side='top', fill='x', pady=10)

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


