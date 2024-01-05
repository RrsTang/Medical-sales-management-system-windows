import tkinter.ttk as ttk
from gui.head_info import *
from tkinter import messagebox


def room_page(master, func, handle):
    title = tk.Label(master, text='房间信息管理系统', font=('fangsong ti', 16, 'bold'), bg='white') \
        .pack(fill='x', side='top', pady=10)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree = ttk.Treeview(master, show='headings', height=500)
    tree["columns"] = ("房间号", "房间类型", "单价", "房间状态", "入住客户", "联系方式-a", "预定客户", "预定时间", "联系方式")
    tree.column("房间号", width=50, anchor='center')
    tree.column("房间类型", width=50, anchor='center')
    tree.column("房间状态", width=50, anchor='center')
    tree.column("单价", width=50, anchor='center')
    tree.column("入住客户", width=50, anchor='center')
    tree.column("联系方式-a", width=100, anchor='center')
    tree.column("预定客户", width=50, anchor='center')
    tree.column("预定时间", width=50, anchor='center')
    tree.column("联系方式", width=100, anchor='center')
    tree.heading("房间号", text="房间号")
    tree.heading("房间类型", text="房间类型")
    tree.heading("房间状态", text="房间状态")
    tree.heading("单价", text='单价')
    tree.heading("入住客户", text="入住客户")
    tree.heading("联系方式-a", text="联系方式")
    tree.heading("预定客户", text="预定客户")
    tree.heading("预定时间", text="预定时间")
    tree.heading("联系方式", text="联系方式")

    room_id = tk.StringVar()
    room_id2 = tk.StringVar()
    room_id3 = tk.StringVar()
    price = tk.StringVar()
    rtype = tk.StringVar()
    new_id = tk.StringVar()
    new_type = tk.StringVar()
    new_price = tk.StringVar()

    def find_by_room_id():
        id = room_id.get()
        y = year.get()
        m = month.get()
        d = day.get()
        try:
            ret = handle.select_room_information_by_id(id, f"{y}-{m}-{d}")
            print(ret)
        except:
            messagebox.showerror(message='未找到相关信息')
            return
        if ret == 0:
            messagebox.showerror(message='未找到相关信息')
            return

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        for i in range(len(ret)):
            tree.insert('', i, values=ret[i])

    def find_by_type():
        type = room_type.get()
        y = year.get()
        m = month.get()
        d = day.get()
        try:
            ret = handle.select_left_rooms_info(type, f"{y}-{m}-{d}")
        except:
            messagebox.showerror(message='没有空闲房间')
            return
        if len(ret) == 0:
            messagebox.showerror(message='没有空闲房间')
            return

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        for i in range(len(ret)):
            tree.insert('', i, values=ret[i])

    def update_price():
        result = tk.messagebox.askquestion('确认操作', '是否修改房间价格')
        if result == 'yes':
            _id = room_id2.get()
            _price = price.get()
            try:
                handle.update_room_price(_id, _price)
                messagebox.showinfo(message='修改成功')
            except:
                messagebox.showerror(message='您无权限进行该操作！')

    def update_type():
        result = tk.messagebox.askquestion('确认操作', '是否修改房间类型')
        if result == 'yes':
            _id = room_id3.get()
            _type = rtype.get()
            try:
                handle.update_room_type(_id, _type)
                messagebox.showinfo(message='修改成功')
            except:
                messagebox.showerror(message='您无权限进行该操作！')


    def delete_by_room_id():
        result = tk.messagebox.askquestion('确认操作', '是否删除该房间！')
        if result == 'yes':
            _id = room_id.get()
            try:
                handle.delete_from_room(_id)
                messagebox.showinfo(message='删除成功')
            except:
                messagebox.showerror(message='您无权限进行该操作！')

    def insert_room():
        result = tk.messagebox.askquestion('确认操作', '是否添加新房间！')
        if result == 'yes':
            _id = new_id.get()
            _type = new_type.get()
            _price = new_price.get()
            try:
                handle.insert_into_room(_id, _price, _type)
                messagebox.showinfo(message='添加成功')
            except:
                messagebox.showerror(message='您无权限进行该操作！')

    def back():
        master.destroy()
        func()

    search_line_date = tk.Frame(master, bg="white")
    year = tk.StringVar()
    month = tk.StringVar()
    day = tk.StringVar()
    year.set(datetime.now().year)
    month.set(datetime.now().month)
    day.set(datetime.now().day)
    yearlist = ttk.Combobox(search_line_date, textvariable=year, width=6)
    yearlist["values"] = ('2020', '2021', '2022')
    # yearlist.current(1)
    monthlist = ttk.Combobox(search_line_date, textvariable=month, width=6)
    monthlist["values"] = ('',) + tuple([i for i in range(1, 13)])
    daylist = ttk.Combobox(search_line_date, textvariable=day, width=6)
    daylist["values"] = ('',) + tuple([i for i in range(1, 32)])

    yearlist.pack(side='left', padx=(15, 5))
    tk.Label(search_line_date, text='年', font=('song ti', 9), bg='white').pack(side='left', padx=(0, 5))
    monthlist.pack(side='left', padx=(0, 5))
    tk.Label(search_line_date, text='月', font=('song ti', 9), bg='white').pack(side='left', padx=(0, 5))
    daylist.pack(side='left', padx=(0, 5))
    tk.Label(search_line_date, text='日', font=('song ti', 9), bg='white').pack(side='left', padx=(0, 5))
    tk.Button(search_line_date, text='返回', font=('song ti', 9), bg='#4ABD96', fg="#FFFFFF", bd=1, command=back, width=5) \
        .pack(side='right', padx=(0, 20))

    search_line_date.pack(side='top', fill='x', pady=5)

    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    search_line0 = tk.Frame(master, bg="white")
    tk.Label(search_line0, text='空闲房间查询  房间类型:', font=('song ti', 9), bg='white').pack(side='left', padx=(10, 0))
    room_type = tk.StringVar()
    comlist = ttk.Combobox(search_line0, textvariable=room_type, width=10)
    comlist["values"] = ('', "单人房", "双人房", "大床房")
    comlist.current(0)
    comlist.pack(side='left', padx=(5, 10))
    tk.Button(search_line0, text='查询', font=('song ti', 9), bd=1, command=find_by_type, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left')
    search_line0.pack(side='top', fill='x', pady=5)

    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    search_line1 = tk.Frame(master, bg='white')
    tk.Label(search_line1, text='房间状态查询    房间号：', bg='white', font=('song ti', 9)).pack(side='left', padx=(10, 0))
    tk.Entry(search_line1, textvariable=room_id, width=8, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 10))

    tk.Button(search_line1, text='查询', font=('song ti', 9), bd=1, command=find_by_room_id, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left', padx=(0, 10))

    tk.Button(search_line1, text='删除该房间', font=('song ti', 9), bd=1, command=delete_by_room_id, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left')
    search_line1.pack(fill='x', side='top', pady=5)

    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    update_line1 = tk.Frame(master, bg='white')
    tk.Label(update_line1, text='房间价格修改    房间号：', bg='white', font=('song ti', 9)).pack(side='left', padx=(10, 0))
    tk.Entry(update_line1, textvariable=room_id2, width=8, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 10))
    tk.Label(update_line1, text='房间价格：', bg='white', font=('song ti', 9)).pack(side='left', padx=(10, 0))
    tk.Entry(update_line1, textvariable=price, width=6, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 10))
    tk.Button(update_line1, text='修改', font=('song ti', 9), bd=1, command=update_price, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left')
    update_line1.pack(side='top', fill='x', pady=5)

    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    update_line2 = tk.Frame(master, bg='white')
    tk.Label(update_line2, text='房间类型修改    房间号：', bg='white', font=('song ti', 9)).pack(side='left', padx=(10, 0))
    tk.Entry(update_line2, textvariable=room_id3, width=8, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 10))
    tk.Label(update_line2, text='房间类型：', bg='white', font=('song ti', 9)).pack(side='left', padx=(10, 0))
    tk.Entry(update_line2, textvariable=rtype, width=6, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 10))
    tk.Button(update_line2, text='修改', font=('song ti', 9), bd=1, command=update_type, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left')
    update_line2.pack(side='top', fill='x', pady=5)

    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    insert_line = tk.Frame(master, bg='white')
    tk.Label(insert_line, text='创建房间  房间号：', bg='white', font=('song ti', 9)).pack(side='left', padx=(10, 0))
    tk.Entry(insert_line, textvariable=new_id, width=6, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 10))
    tk.Label(insert_line, text='房间类型：', bg='white', font=('song ti', 9)).pack(side='left', padx=(10, 0))
    tk.Entry(insert_line, textvariable=new_type, width=6, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 10))
    tk.Label(insert_line, text='房间价格：', bg='white', font=('song ti', 9)).pack(side='left', padx=(10, 0))
    tk.Entry(insert_line, textvariable=new_price, width=6, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 10))
    tk.Button(insert_line, text='创建', font=('song ti', 9), bd=1, command=insert_room, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left')
    insert_line.pack(side='top', fill='x', pady=5)

    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree.pack(side='top', fill='x')


if __name__ == '__main__':
    root = tk.Tk()
