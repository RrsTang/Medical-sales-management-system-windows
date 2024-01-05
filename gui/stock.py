import tkinter.ttk as ttk
from gui.head_info import *
from tkinter import messagebox


def stoke_page(master, func, handle):
    title = tk.Label(master, text='进货管理', font=('fangsong ti', 18, 'bold'), bg='white') \
        .pack(fill='x', side='top', pady=10)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree = ttk.Treeview(master, show='headings', height=500)
    tree["columns"] = ("进货记录ID", "药品ID", "仓库ID", "供应商ID", "进货数量", "进货价格", "进货日期")
    tree.column("进货记录ID", width=50, anchor='center')
    tree.column("药品ID", width=50, anchor='center')
    tree.column("仓库ID", width=50, anchor='center')
    tree.column("供应商ID", width=50, anchor='center')
    tree.column("进货数量", width=50, anchor='center')
    tree.column("进货价格", width=50, anchor='center')
    tree.column("进货日期", width=50, anchor='center')
    tree.heading("进货记录ID", text="进货记录ID")
    tree.heading("药品ID", text="药品ID")
    tree.heading("仓库ID", text="仓库ID")
    tree.heading("供应商ID", text='供应商ID')
    tree.heading("进货数量", text="进货数量")
    tree.heading("进货价格", text="进货价格")
    tree.heading("进货日期", text="进货日期")

    stock_id1 = tk.StringVar()
    stock_id2 = tk.StringVar()
    medicine_id = tk.StringVar()
    warehouse_id = tk.StringVar()
    supplier_id = tk.StringVar()
    num = tk.StringVar()
    price = tk.StringVar()
    year = tk.StringVar()
    month = tk.StringVar()
    day = tk.StringVar()

    def find_by_stock_id():
        id = stock_id1.get()
        try:
            ret = handle.select_stock_by_id(id)
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

    def find_stock_all():
        try:
            ret = handle.select_stock_all()
        except:
            messagebox.showerror(message='未找到相关信息')
            return
        if len(ret) == 0:
            messagebox.showerror(message='未找到相关信息')
            return
        print(ret)
        x = tree.get_children()
        for item in x:
            tree.delete(item)
        for i in range(len(ret)):
            tree.insert('', i, values=ret[i])

    def insert_stock():
        result = tk.messagebox.askquestion('确认操作', '是否添加新记录！')
        if result == 'yes':
            _stock_id = stock_id2.get()
            _medicine_id = medicine_id.get()
            _warehouse_id = warehouse_id.get()
            _supplier_id = supplier_id.get()
            _num = num.get()
            _price = price.get()
            _year =year.get()
            _month =month.get()
            _day =day.get()
            try:
                ret=handle.insert_into_stock(_stock_id, _medicine_id, _warehouse_id,_supplier_id,_num,_price,_year,_month,_day)
                if ret=='True':
                    messagebox.showinfo(message='添加成功')
                else:
                    messagebox.showinfo(message=ret)
            except:
                messagebox.showerror(message='您无权限进行该操作！')

    def back():
        master.destroy()
        func()

    search_line1 = tk.Frame(master, bg='white')
    tk.Label(search_line1, text='进货记录查询    进货记录ID：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(search_line1, textvariable=stock_id1, width=8, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 15))
    tk.Button(search_line1, text='查询', font=('song ti', 13), bd=2, command=find_by_stock_id, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left', padx=(0, 15))
    tk.Button(search_line1, text='查询所有', font=('song ti', 13), bd=2, command=find_stock_all, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left', padx=(0, 15))
    tk.Button(search_line1, text='返回', font=('song ti', 13), bg='#058AF3', fg="#FFFFFF", bd=2, command=back, width=5) \
        .pack(side='right', padx=(0, 20))
    search_line1.pack(fill='x', side='top', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    insert_line = tk.Frame(master, bg='white')
    tk.Label(insert_line, text='添加记录  进货记录ID：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(insert_line, textvariable=stock_id2, width=6, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 15))
    tk.Label(insert_line, text='药品ID：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(insert_line, textvariable=medicine_id, width=6, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 15))
    tk.Label(insert_line, text='仓库ID：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(insert_line, textvariable=warehouse_id, width=6, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 15))
    tk.Label(insert_line, text='供应商ID：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(insert_line, textvariable=supplier_id, width=6, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 15))
    insert_line.pack(side='top', fill='x', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    insert_line2 = tk.Frame(master, bg='white')
    tk.Label(insert_line2, text='进货数量：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(insert_line2, textvariable=num, width=6, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 15))
    tk.Label(insert_line2, text='进货价格：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(insert_line2, textvariable=price, width=6, bd=0, font=('song ti', 13), bg='lightsteelblue') \
        .pack(side='left', padx=(0, 15))
    tk.Label(insert_line2, text='进货日期：', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))

    year.set(datetime.now().year)
    month.set(datetime.now().month)
    day.set(datetime.now().day)
    yearlist = ttk.Combobox(insert_line2, textvariable=year, width=6)
    yearlist["values"] = ('2023', '2022', '2021')
    # yearlist.current(1)
    monthlist = ttk.Combobox(insert_line2, textvariable=month, width=6)
    monthlist["values"] = ('',) + tuple([i for i in range(1, 13)])
    daylist = ttk.Combobox(insert_line2, textvariable=day, width=6)
    daylist["values"] = ('',) + tuple([i for i in range(1, 32)])
    yearlist.pack(side='left', padx=(15, 5))
    tk.Label(insert_line2, text='年', font=('song ti', 13), bg='white').pack(side='left', padx=(0, 5))
    monthlist.pack(side='left', padx=(0, 5))
    tk.Label(insert_line2, text='月', font=('song ti', 13), bg='white').pack(side='left', padx=(0, 5))
    daylist.pack(side='left', padx=(0, 5))
    tk.Label(insert_line2, text='日', font=('song ti', 13), bg='white').pack(side='left', padx=(0, 5))

    tk.Button(insert_line2, text='添加', font=('song ti', 13), bd=2, command=insert_stock, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left')
    insert_line2.pack(side='top', fill='x', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree.pack(side='top', fill='x')


if __name__ == '__main__':
    root = tk.Tk()
