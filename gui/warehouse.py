import tkinter.ttk as ttk
from gui.head_info import *
from gui.config import *
from sql_handler.handler import handler
from tkinter import messagebox


def warehouse(master, func, handle):
    title = tk.Label(master, text='仓库', font=('fangsong ti', 18, 'bold'), bg='white')\
        .pack(fill='x', side='top', pady=10)
    Separator(master, orient='horizontal').pack(side='top', fill='x')
    tree_and_scrollbar = tk.Frame(master, bg='white')
    ys = ttk.Scrollbar(tree_and_scrollbar, orient='vertical')
    tree = ttk.Treeview(tree_and_scrollbar, show='headings', height=500, yscrollcommand=ys.set)
    ys['command'] = tree.yview
    tree["columns"] = ("仓库ID", "药品ID", "药名", "数量")
    tree.column("仓库ID", width=120, anchor='center')
    tree.column("药品ID", width=120, anchor='center')
    tree.column("药名", width=70, anchor='center')
    tree.column("数量", width=50, anchor='center')
    
    tree.heading("仓库ID", text="仓库ID")
    tree.heading("药品ID", text="药品ID")
    tree.heading("药名", text="药名")
    tree.heading("数量", text='数量')

    medi_id = tk.StringVar()
    medi_name = tk.StringVar()
    new_id = tk.StringVar()
    new_addr = tk.StringVar()

    def find_all():
        try:
            ret = handle.select_warehouse_all()
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

    def find_by_id(event=None):
        id = medi_id.get()
        try:
            ret = handle.select_warehouse_information_by_id(id)
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
        name = medi_name.get()
        try:
            ret = handle.select_warehouse_information_by_name(name)
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

    def insert_warehouse(event=None):
        id_ = new_id.get()
        addr = new_addr.get()
        try:
            handle.insert_warehouse(id_, addr)
            messagebox.showinfo(message='添加成功')
        except:
            messagebox.showerror(message='添加失败')

    def back():
        master.destroy()
        func()

    search_line = tk.Frame(master, bg='white')

    tk.Label(search_line, text='药品ID:', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    identry = tk.Entry(search_line, textvariable=medi_id, width=25, bd=0, font=myFont, bg='lightsteelblue')
    identry.bind('<Return>', find_by_id)
    identry.pack(side='left', padx=(0, 15))
    tk.Button(search_line, text='查询', font=('song ti', 13), bd=2, command=find_by_id, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left',padx=(0, 15))
    search_line.pack(side='top', fill='x', pady=5)
    tk.Button(search_line, text='查询所有', font=('song ti', 13), bd=2, command=find_all, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left')
    search_line.pack(side='top', fill='x', pady=5)
    tk.Button(search_line, text='返回', font=('song ti', 13), bg='#058AF3',fg="#FFFFFF", bd=2, command=back, width=5)\
        .pack(side='right', padx=(0, 20))
    search_line.pack(fill='x', side='top', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    search_line0 = tk.Frame(master, bg='white')
    tk.Label(search_line0, text='药  名:', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    identry = tk.Entry(search_line0, textvariable=medi_name, width=25, bd=0, font=myFont, bg='lightsteelblue')
    identry.bind('<Return>', find_by_name)
    identry.pack(side='left', padx=(0, 15))
    tk.Button(search_line0, text='查询', font=('song ti', 13), bd=2, command=find_by_name, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left',padx=(0, 20))
    search_line0.pack(fill='x', side='top', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')

    search_line1 = tk.Frame(master, bg='white')
    tk.Label(search_line1, text='添加新仓库:   id:', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    identry = tk.Entry(search_line1, textvariable=new_id, width=25, bd=0, font=myFont, bg='lightsteelblue').pack(side='left', padx=(0, 15))
    tk.Label(search_line1, text='地址:', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    identry = tk.Entry(search_line1, textvariable=new_addr, width=25, bd=0, font=myFont, bg='lightsteelblue').pack(side='left', padx=(0, 15))
    tk.Button(search_line1, text='添加', font=('song ti', 13), bd=2, command=insert_warehouse, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left',padx=(0, 20))
    search_line1.pack(fill='x', side='top', pady=5)
    
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')
    tree.pack(side='left', fill='x', expand=1)
    ys.pack(side='right', fill='y', anchor='w')
    tree_and_scrollbar.pack(side='top', fill='x', expand=1)


if __name__ == '__main__':
    root = tk.Tk()