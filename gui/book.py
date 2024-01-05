import tkinter as tk
import pymysql
from tkinter import ttk
from tkinter import messagebox  # tkinter 弹窗
from gui.config import *
from gui.head_info import *
import time

def book_page(master, func, handle):
    cid1 = tk.StringVar()
    cname1 = tk.StringVar()
    tel1 = tk.StringVar()
    sex1 = tk.StringVar()
    cid2 = tk.StringVar()
    cname2 = tk.StringVar()
    tel2 = tk.StringVar()
    sex2 = tk.StringVar()
    year = tk.StringVar()
    month = tk.StringVar()
    day = tk.StringVar()
    roomType = tk.StringVar()
    roomID = "待定"
    treeSize = 0

    def back():
        master.destroy()
        func()
        pass

    def update_time():
        now = datetime.now()
        text = '时间：%s-%s-%s  %s:%s:%s' % \
               (
                   now.year,
                   '{:0>2d}'.format(now.month),
                   '{:0>2d}'.format(now.day),
                   '{:0>2d}'.format(now.hour),
                   '{:0>2d}'.format(now.minute),
                   '{:0>2d}'.format(now.second)
               )
        # nowTime.set(text)
        # lb.after(1, update_time)
        print(1)

    update_time()

    def mydate():
        """
        confirm时就将顾客信息插入到顾客表里
        :return: None
        """
        try:
            intime = time.strptime(f'{year.get()}-{month.get()}-{day.get()}', '%Y-%m-%d')
        except:
            tk.messagebox.showerror(message='日期错误，请检查日期')
            return

    def confirm():
        """
        confirm时就将顾客信息插入到顾客表里
        :return: None
        """
        try:
            intime = time.strptime(f'{year.get()}-{month.get()}-{day.get()}', '%Y-%m-%d')
        except:
            tk.messagebox.showerror(message='日期错误，请检查日期')
            return
        if intime < time.strptime(f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}', '%Y-%m-%d'):
            tk.messagebox.showerror(message='日期错误，请检查日期')
            return
        if cid1.get() == "" or cname1.get() == '' or sex1.get() == '' or tel1.get() == '':
            tk.messagebox.showerror(message="请输入完整信息")
            return
        if roomType.get() == "单人房" and cid2.get() != "":
            tk.messagebox.showerror(message="单人房仅支持一个人")
            return
        record = [roomType.get(), cid1.get(), cname1.get(), sex1.get(), tel1.get(), cid2.get(), cname2.get(),
                  sex2.get(), tel2.get(), roomID]

        nonlocal treeSize
        tree.insert('', treeSize, values=record)
        treeSize += 1
        cid1.set("")
        cname1.set("")
        tel1.set("")
        sex1.set("")
        cid2.set("")
        cname2.set("")
        tel2.set("")
        sex2.set("")
        pass


    def submit():
        """
        1. 检查房间剩余数量是否足够
        2. 生成流水号
        3. 获得房间信息
        item = ("type, cid1, 姓名1, sex1, tel1, cid2, 姓名2, sex2, tel2, 房间号")
        :return: None
        """
        # serialNum = None
        records = tree.get_children()
        print(records)
        if len(records) == 0:
            tk.messagebox.showerror(message=f"你没有输入任何信息")
            return
        date = f'{year.get()}-{month.get()}-{day.get()}'
        # 1. 分别检查房间剩余数量是否足够
        num_single = len(handle.select_left_rooms_info("单人房", date))
        num_double = len(handle.select_left_rooms_info("双人房", date))
        num_big = len(handle.select_left_rooms_info("大床房", date))
        dic = {"单人房": num_single, "双人房": num_double, "大床房": num_big}
        for item in records:
            dic[tree.item(item, "values")[0]] -= 1
        if dic["单人房"] < 0 or dic["双人房"] < 0 or dic["大床房"] < 0:
            tk.messagebox.showerror(message=f"房间数量不足，请前往查询页面查看房间详情")
            return
        # 2. 插入顾客
        print(item)
        for item in records:
            info = tree.item(item, "values")
            print(info)
            try:
                print(info[1], info[2], info[3], info[4])
                ret = handle.insert_into_customer(info[1], info[2], info[3], info[4])
                print("err")
                if ret == 'change':
                    tk.messagebox.showinfo(message=f"顾客{info[2]}信息已变更")
            except Exception as e:
                tk.messagebox.showinfo(message=f"插入顾客{info[2]}时错误：{e}")
            if info[0] == "双人房" or info[0] == "大床房":
                try:
                    ret = handle.insert_into_customer(info[5], info[6], info[7], info[8])
                    if ret == 'change':
                        tk.messagebox.showinfo(message=f"顾客{info[6]}信息已变更")
                except Exception as e:
                    tk.messagebox.showinfo(message=f"插入顾客{info[6]}时错误：{e}")
        # 3. 生成流水号
        try:
            # 默认第一个cid1是该流水号的leader
            serialNum = handle.insert_sequenceInfo(date, tree.item(records[0], "values")[1])
        except Exception as e:
            tk.messagebox.showerror(message=f"获取新的流水失败{e}")
            return
        # 4. 加入房间信息stay
        for i in range(len(records)):
            # insert into stay
            item = records[i]
            print(item, ":", tree.item(item, "values"))
            paras = list(tree.item(item, "values"))
            newroom = handle.insert_into_stay(serialNum, date, paras)
            # 修改tree的房间号
            paras[9] = newroom
            tree.delete(item)
            tree.insert('', i, values=paras)
            pass
        tk.messagebox.showinfo(message=f"完成预定，房间信息见表格，流水号为{serialNum}")
        # 如果是今天的，可以选择立即入住
        if date == f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}':
            result = tk.messagebox.askquestion('确认操作', '是否立即入住')
            if result == 'yes':
                handle.live_in(serialNum)
                messagebox.showinfo("", "入住成功")
        btn_genSerial.pack_forget()
        line2.pack_forget()
        frame1.pack_forget()
        frame2.pack_forget()
        buttonLine.pack_forget()

    def isSingle(para=None):
        if roomType.get() == '双人房' or roomType.get() == '大床房':
            tree.pack_forget()
            buttonLine.pack_forget()
            frame2.pack(side='top', fill='x', pady=(0, 10))
            buttonLine.pack(side='top', fill='x', pady=(0, 10))
            tree.pack(side='bottom', fill='x')
        else:
            frame2.pack_forget()

    def delete_choose(event=None):
        item = tree.focus()
        if item is None:
            messagebox.showerror(message='未选中数据')
            return
        tree.delete(item)

    def load_customer1(para=None):
        info = handle.select_customer_basic_info_by_id(cid1.get())
        if len(info) == 0:
            cname1.set("")
            sex1.set("")
            tel1.set("")
            return
        cname1.set(info[0][1])
        sex1.set(info[0][2])
        tel1.set(info[0][3])

    def load_customer2(para=None):
        info = handle.select_customer_basic_info_by_id(cid2.get())
        if len(info) == 0:
            cname2.set("")
            sex2.set("")
            tel2.set("")
            return
        cname2.set(info[0][1])
        sex2.set(info[0][2])
        tel2.set(info[0][3])

    # 宾馆信息
    print(day)
    print(1)
    # my = time.strptime(f'{year.get()}-{month.get()}-{day.get()}', '%Y-%m-%d')
    bg = '#2B2B2B'
    fg = '#FFC665'
    now = datetime.now()
    currDate = f"{now.year}-{now.month}-{now.day}"
    hotel_info = tk.Frame(master, bg=bg)
    left = 40
    right = 30
    ret = handle.select_left_rooms_count(currDate)
    left_single = 0
    left_double = 0
    left_big = 0
    for item in ret:
        if item[0] == '单人房':
            left_single = item[1]
        elif item[0] == '双人房':
            left_double = item[1]
        else:
            left_big = item[1]
    # 剩余单人间
    lb1 = tk.Label(hotel_info, fg=fg, bg=bg, text='剩余单人房： {:d} '.format(left_single), font=myFont).pack(side='top',
    anchor='nw',padx=10,pady=(140, 50))

    # 剩余双人间
    lb2 = tk.Label(hotel_info, fg=fg, bg=bg, text='剩余双人房： {:d} '.format(left_double), font=myFont).pack(side='top',
    anchor='nw',padx=10,pady=(0, 50))

    # 剩余大床房
    lb3 = tk.Label(hotel_info, fg=fg, bg=bg, text='剩余大床房： {:d} '.format(left_big), font=myFont).pack(side='top',
    anchor='nw',padx=10,pady=(0, 50))


    hotel_info.pack(side='left', fill='y')

    fonts = ("song ti", 13)
    head = tk.Frame(master, bg='white')
    # title = tk.Label(head, text='房间预订', font=('fangsong ti', 18, 'bold'), bg='white').pack(fill='x', side='left', pady=10, padx=20)


    head.pack(side='top', fill='x')

    line2 = tk.Frame(master, bg='white')
    tk.Label(line2, text='房间类型：', font=('song ti', 13), bg='white').pack(side='left', padx=(10, 5),pady=10)
    com = ttk.Combobox(line2, textvariable=roomType, width=10)  # #创建下拉菜单
    com.bind("<FocusIn>", isSingle)
    com.pack(side='left', padx=(5, 5))  # #将下拉菜单绑定到窗体
    com["value"] = ("单人房", "双人房", "大床房")  # #给下拉菜单设定值
    com.current(0)
    year.set(datetime.now().year)
    month.set(datetime.now().month)
    day.set(datetime.now().day)
    yearlist = ttk.Combobox(line2, textvariable=year, width=6)
    yearlist["values"] = ('2022', '2023', '2024')
    monthlist = ttk.Combobox(line2, textvariable=month, width=6)
    monthlist["values"] = ('',) + tuple([i for i in range(1, 13)])
    daylist = ttk.Combobox(line2, textvariable=day, width=6)
    daylist["values"] = ('',) + tuple([i for i in range(1, 32)])
    yearlist.pack(side='left', padx=(15, 5))
    tk.Label(line2, text='年', font=('song ti', 13), bg='white').pack(side='left', padx=(0, 5))
    monthlist.pack(side='left', padx=(0, 5))
    tk.Label(line2, text='月', font=('song ti', 13), bg='white').pack(side='left', padx=(0, 5))
    daylist.pack(side='left', padx=(0, 5))
    tk.Label(line2, text='日', font=('song ti', 13), bg='white').pack(side='left', padx=(0, 5))
    line2.pack(side='top', fill='x')

    frame1 = tk.Frame(master, bg='white')
    tk.Label(frame1, text='身份证号：', bg='white', font=fonts).pack(side='left', padx=(10, 0),pady=10)
    cid_entry1 = tk.Entry(frame1, textvariable=cid1, width=20, bd=0, font=fonts, bg='lightsteelblue')
    cid_entry1.pack(side='left', padx=(0, 5))
    cid_entry1.bind('<FocusOut>', load_customer1)
    cid_entry1.bind("<Return>", load_customer1)
    # cid_entry1.bind("<Tab>", load_customer1)

    tk.Label(frame1, text='姓名：', bg='white', font=fonts).pack(side='left', padx=(10, 0))
    tk.Entry(frame1, textvariable=cname1, width=8, bd=0, font=fonts, bg='lightsteelblue') \
        .pack(side='left', padx=(0, 5))

    tk.Label(frame1, text='电话：', bg='white', font=fonts).pack(side='left', padx=(10, 0))
    tk.Entry(frame1, textvariable=tel1, width=13, bd=0, font=fonts, bg='lightsteelblue') \
        .pack(side='left', padx=(0, 5))

    tk.Label(frame1, text='性别：', bg='white', font=fonts).pack(side='left', padx=(10, 0))
    boxSex1 = ttk.Combobox(frame1, textvariable=sex1, width=3)  # #创建下拉菜单
    boxSex1.pack(side='left', padx=(0, 5))  # #将下拉菜单绑定到窗体
    boxSex1["value"] = ("男", "女")  # #给下拉菜单设定值
    boxSex1.current(0)
    frame1.pack(side='top', fill='x', pady=10)

    frame2 = tk.Frame(master, bg='white')
    tk.Label(frame2, text='身份证号：', bg='white', font=fonts).pack(side='left', padx=(10, 0))
    cid_entry2 = tk.Entry(frame2, textvariable=cid2, width=20, bd=0, font=fonts, bg='lightsteelblue')
    cid_entry2.pack(side='left', padx=(0, 5))
    cid_entry2.bind('<FocusOut>', load_customer2)
    cid_entry2.bind("<Return>", load_customer2)
    # cid_entry2.bind("<Tab>", load_customer2)

    tk.Label(frame2, text='姓名：', bg='white', font=fonts).pack(side='left', padx=(10, 0))
    tk.Entry(frame2, textvariable=cname2, width=8, bd=0, font=fonts, bg='lightsteelblue') \
        .pack(side='left', padx=(0, 5))

    tk.Label(frame2, text='电话：', bg='white', font=fonts).pack(side='left', padx=(10, 0))
    tk.Entry(frame2, textvariable=tel2, width=13, bd=0, font=fonts, bg='lightsteelblue') \
        .pack(side='left', padx=(0, 5))

    tk.Label(frame2, text='性别：', bg='white', font=fonts).pack(side='left', padx=(10, 0))
    boxSex2 = ttk.Combobox(frame2, textvariable=sex2, width=3)  # #创建下拉菜单
    boxSex2.pack(side='left', padx=(0, 5))  # #将下拉菜单绑定到窗体
    boxSex2["value"] = ("男", "女")  # #给下拉菜单设定值
    # frame2.pack(side='top', fill='x')
    # frame2.pack_forget()

    buttonLine = tk.Frame(master, bg='white')

    tk.Button(buttonLine, text='添加顾客信息', font=('song ti', 13), bd=2, command=confirm, fg="#F6FDFE", bg='#058AF3', width=15).pack(
        side='left', padx=20,pady=10)

    btn_genSerial = tk.Button(buttonLine, text='确认预订', font=('song ti', 13), bd=2, fg="#F6FDFE", bg='#058AF3', command=submit, width=12)
    btn_genSerial.pack(side='left', padx=10)


    tk.Button(buttonLine, text='删除选中行', font=('song ti', 13), bd=2, command=delete_choose, fg="#F6FDFE",bg='#ED5252', width=13) \
        .pack(side='left', padx=20)

    buttonLine.pack(side='top', fill='x', pady=(0, 10))
    tk.Button(buttonLine, text='返回', font=('song ti', 13), bd=2, bg='#4ABD96', fg="#FFFFFF", command=back, width=5).pack(
        side='right', padx=60)
    tree = ttk.Treeview(master, show='headings', height=500)
    tree["columns"] = ("房间类型", "顾客1", "姓名1", "性别1", "电话1", "顾客2", "姓名2", "性别2", "电话2", "房间号")
    tree.column("房间类型", width=50, anchor='center')
    tree.column("顾客1", width=100, anchor='center')
    tree.column("姓名1", width=50, anchor='center')
    tree.column("性别1", width=30, anchor='center')
    tree.column("电话1", width=70, anchor='center')
    tree.column("顾客2", width=100, anchor='center')
    tree.column("姓名2", width=50, anchor='center')
    tree.column("性别2", width=30, anchor='center')
    tree.column("电话2", width=70, anchor='center')
    tree.column("房间号", width=30, anchor='center')
    tree.heading("房间类型", text="房间类型")
    tree.heading("顾客1", text="顾客1id")
    tree.heading("姓名1", text="姓名")
    tree.heading("性别1", text='性别')
    tree.heading("电话1", text="电话")
    tree.heading("顾客2", text="顾客2id")
    tree.heading("姓名2", text="姓名")
    tree.heading("性别2", text="性别")
    tree.heading("电话2", text="电话")
    tree.heading("房间号", text="房间号")
    tree.pack(side='bottom', fill='x')


if __name__ == '__main__':
    root = tk.Tk()


