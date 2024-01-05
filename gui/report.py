import datetime
import tkinter as tk
from gui.config import *
import tkinter.ttk as ttk
from gui.head_info import *

def report_main_page(master, mode, hd, handle=None):
    def return_finance():
        mode.set("financial")
        handle()

    def return_stock():
        mode.set("stock")
        handle()

    def return_sales():
        mode.set("sales")
        handle() 

    def return_warehouse():
        mode.set("warehouse")
        handle()

    def return_report_main():
        mode.set("exit")
        handle()

    bg = '#F0F0F0'

    # 操作菜单
    menus = tk.Frame(master, bg=bg)
    left = 50
    right = 50
    bold_font = ('song ti', 16, 'bold')
    button_fg = '#ffc66d'
    button_bg = '#44615D'
    button_highlightthickness = 2
    button_highlightbackground = '#688A7E'
    tk.Button(menus, text='财务报表', font=bold_font, height=2,width=25, bd=4, fg=button_fg,
                     activebackground='white', bg=button_bg, command=return_finance)\
        .pack(side='top', padx=(left, right), pady=(100, 30))
    tk.Button(menus, text='入库报表', font=bold_font, height=2,width=25, bd=4, fg=button_fg,
                     activebackground='white', bg=button_bg, command=return_stock) \
        .pack(side='top', padx=(left, right), pady=(0, 30))
    tk.Button(menus, text='销售报表', font=bold_font, height=2,width=25, bd=4, fg=button_fg,
                     activebackground='white', bg=button_bg, command=return_sales) \
        .pack(side='top', padx=(left, right), pady=(0, 30))
    tk.Button(menus, text='仓库报表', font=bold_font, height=2,width=25, bd=4, fg=button_fg,
                     activebackground='white', bg=button_bg, command=return_warehouse) \
        .pack(side='top', padx=(left, right), pady=(0, 30))
    tk.Button(menus, text='返回', font=bold_font, height=2,width=25, bd=4, fg=button_fg,
                     activebackground='white', bg='#ad0600', command=return_report_main) \
        .pack(side='top', padx=(left, right), pady=(0, 70))

    menus.pack(side='left', fill='y', expand=True)

def report_finance_page(master, return_to_report_main_handle, handle):
    title = tk.Label(master, text='报表系统：财务报表', font=('fangsong ti', 18, 'bold'), bg='white')\
        .pack(fill='x', side='top', pady=10)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree = ttk.Treeview(master, show='headings', height=500)
    tree["columns"] = ("药物ID", "药物名称", "总数量", "总收入", "仓储-数量", "仓储-收入", "销售-数量", "销售-收入")
    tree.column("药物ID", width=100, anchor='center')
    tree.column("药物名称", width=50, anchor='center')
    tree.column("总收入", width=50, anchor='center')
    tree.column("总数量", width=50, anchor='center')
    tree.column("仓储-数量", width=50, anchor='center')
    tree.column("仓储-收入", width=50, anchor='center')
    tree.column("销售-数量", width=50, anchor='center')
    tree.column("销售-收入", width=50, anchor='center')
    tree.heading("药物ID", text="药物ID")
    tree.heading("药物名称", text="药物名称")
    tree.heading("总收入", text="总收入")
    tree.heading("总数量", text="总数量")
    tree.heading("仓储-数量", text="仓储-数量")
    tree.heading("仓储-收入", text="仓储-收入")
    tree.heading("销售-数量", text="销售-数量")
    tree.heading("销售-收入", text="销售-收入")


    def look_by_day():
        date = datetime.today()

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        sql_results = handle.select_income_by_date(f"{date.year}-{date.month}-{date.day}")
        tree_index = 0
        if len(sql_results) == 0:
            tree.insert('', tree_index, values=(0, 0, 0, 0, 0, 0, 0, 0))
        else:
            for sql_result in sql_results:
                new_result = (sql_result[0], sql_result[1], sql_result[2] - sql_result[4], sql_result[3] - sql_result[5], sql_result[2], sql_result[3], sql_result[4], sql_result[5])
                tree.insert('', tree_index, values=new_result)
                tree_index += 1

    # 从上个月开始查询每月收入
    def look_by_month():
        date = datetime.today()
        year = date.year
        month = date.month

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        sql_results = handle.select_income_by_month(year, month)
        tree_index = 0
        if len(sql_results) == 0:
            tree.insert('', tree_index, values=(0, 0, 0, 0, 0, 0, 0, 0))
        else:
            for sql_result in sql_results:
                new_result = (sql_result[0], sql_result[1], sql_result[2] - sql_result[4], sql_result[3] - sql_result[5], sql_result[2], sql_result[3], sql_result[4], sql_result[5])
                tree.insert('', tree_index, values=new_result)
                tree_index += 1

    def look_by_year():
        year = datetime.now().year
        x = tree.get_children()
        for item in x:
            tree.delete(item)

        sql_results = handle.select_income_by_year(year)
        tree_index = 0
        if len(sql_results) == 0:
            tree.insert('', tree_index, values=(0, 0, 0, 0, 0, 0, 0, 0))
        else:
            for sql_result in sql_results:
                new_result = (sql_result[0], sql_result[1], sql_result[2] - sql_result[4], sql_result[3] - sql_result[5], sql_result[2], sql_result[3], sql_result[4], sql_result[5])
                tree.insert('', tree_index, values=new_result)
                tree_index += 1


    def back():
        master.destroy()
        return_to_report_main_handle()

    search_line = tk.Frame(master, bg='white')

    tk.Button(search_line, text="今日", font=("song ti", 13), bd=2, command=look_by_day, fg="#F6FDFE", bg='#058AF3')\
        .pack(side='left', padx=(10, 10))
    tk.Button(search_line, text="本月", font=("song ti", 13), bd=2, command=look_by_month, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left', padx=(10, 10))
    tk.Button(search_line, text="本年", font=("song ti", 13), bd=2, command=look_by_year, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left', padx=(10, 10))
    tk.Button(search_line, text='返回', font=('song ti', 13), bg='#4ABD96', fg="#FFFFFF", bd=2, command=back, width=5)\
        .pack(side='right', padx=(0, 20))
    search_line.pack(fill='x', side='top', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree.pack(side='top', fill='x')

def report_stock_page(master, return_to_report_main_handle, handle):
    title = tk.Label(master, text='报表系统：入库报表', font=('fangsong ti', 18, 'bold'), bg='white')\
        .pack(fill='x', side='top', pady=10)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree = ttk.Treeview(master, show='headings', height=500)
    tree["columns"] = ("药物ID", "药物名称", "总数量", "总价值")
    tree.column("药物ID", width=100, anchor='center')
    tree.column("药物名称", width=50, anchor='center')
    tree.column("总数量", width=50, anchor='center')
    tree.column("总价值", width=50, anchor='center')
    tree.heading("药物ID", text="药物ID")
    tree.heading("药物名称", text="药物名称")
    tree.heading("总数量", text="总数量")
    tree.heading("总价值", text="总价值")


    def look_by_day():
        date = datetime.today()

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        sql_results = handle.select_stock_by_date(f"{date.year}-{date.month}-{date.day}")
        tree_index = 0
        if len(sql_results) == 0:
            tree.insert('', tree_index, values=(0, 0, 0, 0))
        else:
            for sql_result in sql_results:
                new_result = (sql_result[0], sql_result[1], sql_result[2] - sql_result[4], sql_result[3] - sql_result[5], sql_result[2], sql_result[3], sql_result[4], sql_result[5])
                tree.insert('', tree_index, values=new_result)
                tree_index += 1

    # 从上个月开始查询每月收入
    def look_by_month():
        date = datetime.today()
        year = date.year
        month = date.month

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        sql_results = handle.select_stock_by_month(year, month)
        tree_index = 0
        if len(sql_results) == 0:
            tree.insert('', tree_index, values=(0, 0, 0, 0))
        else:
            for sql_result in sql_results:
                new_result = (sql_result[0], sql_result[1], sql_result[2] - sql_result[4], sql_result[3] - sql_result[5], sql_result[2], sql_result[3], sql_result[4], sql_result[5])
                tree.insert('', tree_index, values=new_result)
                tree_index += 1

    def look_by_year():
        year = datetime.now().year
        x = tree.get_children()
        for item in x:
            tree.delete(item)

        sql_results = handle.select_stock_by_year(year)
        tree_index = 0
        if len(sql_results) == 0:
            tree.insert('', tree_index, values=(0, 0, 0, 0))
        else:
            for sql_result in sql_results:
                new_result = (sql_result[0], sql_result[1], sql_result[2] - sql_result[4], sql_result[3] - sql_result[5], sql_result[2], sql_result[3], sql_result[4], sql_result[5])
                tree.insert('', tree_index, values=new_result)
                tree_index += 1

    def back():
        master.destroy()
        return_to_report_main_handle()

    search_line = tk.Frame(master, bg='white')

    tk.Button(search_line, text="今日", font=("song ti", 13), bd=2, command=look_by_day, fg="#F6FDFE", bg='#058AF3')\
        .pack(side='left', padx=(10, 10))
    tk.Button(search_line, text="本月", font=("song ti", 13), bd=2, command=look_by_month, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left', padx=(10, 10))
    tk.Button(search_line, text="本年", font=("song ti", 13), bd=2, command=look_by_year, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left', padx=(10, 10))
    tk.Button(search_line, text='返回', font=('song ti', 13), bg='#4ABD96', fg="#FFFFFF", bd=2, command=back, width=5)\
        .pack(side='right', padx=(0, 20))
    search_line.pack(fill='x', side='top', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree.pack(side='top', fill='x')

def report_sales_page(master, return_to_report_main_handle, handle):
    title = tk.Label(master, text='报表系统：销售报表', font=('fangsong ti', 18, 'bold'), bg='white')\
        .pack(fill='x', side='top', pady=10)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree = ttk.Treeview(master, show='headings', height=500)
    tree["columns"] = ("药物ID", "药物名称", "总数量", "总价值")
    tree.column("药物ID", width=100, anchor='center')
    tree.column("药物名称", width=50, anchor='center')
    tree.column("总数量", width=50, anchor='center')
    tree.column("总价值", width=50, anchor='center')
    tree.heading("药物ID", text="药物ID")
    tree.heading("药物名称", text="药物名称")
    tree.heading("总数量", text="总数量")
    tree.heading("总价值", text="总价值")


    def look_by_day():
        date = datetime.today()

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        sql_results = handle.select_sales_by_date(f"{date.year}-{date.month}-{date.day}")
        tree_index = 0
        if len(sql_results) == 0:
            tree.insert('', tree_index, values=(0, 0, 0, 0))
        else:
            for sql_result in sql_results:
                new_result = (sql_result[0], sql_result[1], sql_result[2] - sql_result[4], sql_result[3] - sql_result[5], sql_result[2], sql_result[3], sql_result[4], sql_result[5])
                tree.insert('', tree_index, values=new_result)
                tree_index += 1

    # 从上个月开始查询每月收入
    def look_by_month():
        date = datetime.today()
        year = date.year
        month = date.month

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        sql_results = handle.select_sales_by_month(year, month)
        tree_index = 0
        if len(sql_results) == 0:
            tree.insert('', tree_index, values=(0, 0, 0, 0))
        else:
            for sql_result in sql_results:
                new_result = (sql_result[0], sql_result[1], sql_result[2] - sql_result[4], sql_result[3] - sql_result[5], sql_result[2], sql_result[3], sql_result[4], sql_result[5])
                tree.insert('', tree_index, values=new_result)
                tree_index += 1

    def look_by_year():
        year = datetime.now().year
        x = tree.get_children()
        for item in x:
            tree.delete(item)

        sql_results = handle.select_sales_by_year(year)
        tree_index = 0
        if len(sql_results) == 0:
            tree.insert('', tree_index, values=(0, 0, 0, 0))
        else:
            for sql_result in sql_results:
                new_result = (sql_result[0], sql_result[1], sql_result[2] - sql_result[4], sql_result[3] - sql_result[5], sql_result[2], sql_result[3], sql_result[4], sql_result[5])
                tree.insert('', tree_index, values=new_result)
                tree_index += 1

    def back():
        master.destroy()
        return_to_report_main_handle()

    search_line = tk.Frame(master, bg='white')

    tk.Button(search_line, text="今日", font=("song ti", 13), bd=2, command=look_by_day, fg="#F6FDFE", bg='#058AF3')\
        .pack(side='left', padx=(10, 10))
    tk.Button(search_line, text="本月", font=("song ti", 13), bd=2, command=look_by_month, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left', padx=(10, 10))
    tk.Button(search_line, text="本年", font=("song ti", 13), bd=2, command=look_by_year, fg="#F6FDFE", bg='#058AF3') \
        .pack(side='left', padx=(10, 10))
    tk.Button(search_line, text='返回', font=('song ti', 13), bg='#4ABD96', fg="#FFFFFF", bd=2, command=back, width=5)\
        .pack(side='right', padx=(0, 20))
    search_line.pack(fill='x', side='top', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree.pack(side='top', fill='x')

def report_warehouse_page(master, return_to_report_main_handle, handle):
    title = tk.Label(master, text='报表系统：仓库报表', font=('fangsong ti', 18, 'bold'), bg='white')\
        .pack(fill='x', side='top', pady=10)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree = ttk.Treeview(master, show='headings', height=500)
    tree["columns"] = ("仓库ID", "仓库地址", "药物ID", "药物名称", "药物数量")
    tree.column("仓库ID", width=100, anchor='center')
    tree.column("仓库地址", width=50, anchor='center')
    tree.column("药物ID", width=50, anchor='center')
    tree.column("药物名称", width=50, anchor='center')
    tree.column("药物数量", width=50, anchor='center')
    tree.heading("仓库ID", text="仓库ID")
    tree.heading("仓库地址", text="仓库地址")
    tree.heading("药物ID", text="药物ID")
    tree.heading("药物名称", text="药物名称")
    tree.heading("药物数量", text="药物数量")


    def look_by_day():
        date = datetime.today()

        x = tree.get_children()
        for item in x:
            tree.delete(item)

        sql_results = handle.select_warehouse_for_report()
        tree_index = 0
        if len(sql_results) == 0:
            tree.insert('', tree_index, values=(0, 0, 0, 0, 0, 0, 0, 0))
        else:
            for sql_result in sql_results:
                new_result = (sql_result[0], sql_result[1], sql_result[2] - sql_result[4], sql_result[3] - sql_result[5], sql_result[2], sql_result[3], sql_result[4], sql_result[5])
                tree.insert('', tree_index, values=new_result)
                tree_index += 1

    def back():
        master.destroy()
        return_to_report_main_handle()

    search_line = tk.Frame(master, bg='white')

    tk.Button(search_line, text="查询仓储情况", font=("song ti", 13), bd=2, command=look_by_day, fg="#F6FDFE", bg='#058AF3')\
        .pack(side='left', padx=(10, 10))
    tk.Button(search_line, text='返回', font=('song ti', 13), bg='#4ABD96', fg="#FFFFFF", bd=2, command=back, width=5)\
        .pack(side='right', padx=(0, 20))
    search_line.pack(fill='x', side='top', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    tree.pack(side='top', fill='x')

if __name__ == '__main__':
    root = tk.Tk()
