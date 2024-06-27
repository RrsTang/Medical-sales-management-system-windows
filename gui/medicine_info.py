import tkinter.ttk as ttk
from gui.head_info import *
from gui.config import *
from sql_handler.handler import handler
from tkinter import messagebox

# test
def medicine_info(master, func, handle):
    title = tk.Label(master, text='药品信息查询', font=('fangsong ti', 18, 'bold'), bg='white')\
        .pack(fill='x', side='top', pady=10)
    Separator(master, orient='horizontal').pack(side='top', fill='x')
    tree_and_scrollbar = tk.Frame(master, bg='white')
    ys = ttk.Scrollbar(tree_and_scrollbar, orient='vertical')
    tree = ttk.Treeview(tree_and_scrollbar, show='headings', height=500, yscrollcommand=ys.set)
    ys['command'] = tree.yview
    tree["columns"] = ("药品ID", "药名")
    tree.column("药品ID", width=120, anchor='center')
    tree.column("药名", width=70, anchor='center')

    tree.heading("药品ID", text="药品ID")
    tree.heading("药名", text="药名")

    medicine_id = tk.StringVar()
    medicine_name = tk.StringVar()
    change_id = tk.StringVar()
    change_info = tk.StringVar()
    change_item = tk.StringVar()
    mapp = {'药名':'name'}

    def find_all():
        try:
            ret = handle.select_all('medicine')
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
        mid = medicine_id.get()
        try:
            ret = handle.select_information_by_id(mid, 'medicine')
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
        name = medicine_name.get()
        try:
            ret = handle.select_information_by_name(name, 'medicine')
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
    def add_medicine():
        mid = medicine_id.get()
        name = medicine_name.get()
        try:
            succ = handle.add_medicine(mid, name)
            if succ:
                messagebox.showinfo(message='添加成功')
                find_all()
            else:
                messagebox.showerror(message='添加失败')
        except:
            messagebox.showerror(message='添加失败')

    def del_medicine():
        mid = medicine_id.get()
        name = medicine_name.get()
        try:
            succ = handle.del_medicine(mid, name)
            if succ:
                messagebox.showinfo(message='删除成功')
                find_all()
            else:
                messagebox.showerror(message='删除失败')
        except:
            messagebox.showerror(message='删除失败')

    def change_medicine():
        mid = change_id.get()
        name = change_info.get()
        item = mapp[change_item.get()]
        try:
            succ = handle.change_table(mid, name, item, 'medicine')
            if succ:
                messagebox.showinfo(message='更新成功')
                find_all()
            else:
                messagebox.showerror(message='更新失败')
        except Exception as e:
            print(e)
            messagebox.showerror(message='更新失败')

    def back():
        master.destroy()
        func()

    search_line = tk.Frame(master, bg='white')
    # 第一行
    tk.Label(search_line, text='药品ID:', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    identry_id = tk.Entry(search_line, textvariable=medicine_id, width=25, bd=0, font=myFont, bg='lightsteelblue')
    identry_id.bind('<Return>', find_by_id)
    identry_id.pack(side='left', padx=(0, 15))
    tk.Button(search_line, text='查询', font=('song ti', 13), bd=2, command=find_by_id, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left', padx=(0, 15))
    search_line.pack(side='top', fill='x', pady=5)    
    
    
    search_line.pack(side='top', fill='x', pady=5)
    tk.Button(search_line, text='返回', font=('song ti', 13), bg='#058AF3',fg="#FFFFFF", bd=2, command=back, width=5)\
        .pack(side='right', padx=(0, 20))
    search_line.pack(fill='x', side='top', pady=5)
    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')
    # 第二行
    search_line0 = tk.Frame(master, bg='white')
    tk.Label(search_line0, text='药  名:', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    identry_name = tk.Entry(search_line0, textvariable=medicine_name, width=25, bd=0, font=myFont, bg='lightsteelblue')
    identry_name.bind('<Return>', find_by_name)
    identry_name.pack(side='left', padx=(0, 15))
    tk.Button(search_line0, text='查询', font=('song ti', 13), bd=2, command=find_by_name, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left',padx=(0, 15))
    tk.Button(search_line0, text='查询所有', font=('song ti', 13), bd=2, command=find_all, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left', padx=(0, 15))
    tk.Button(search_line0, text='添加', font=('song ti', 13), bd=2, command=add_medicine, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left', padx=(0, 15))
    tk.Button(search_line0, text='删除', font=('song ti', 13), bd=2, command=del_medicine, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left')
    search_line0.pack(fill='x', side='top', pady=5)
    Separator(master, orient='horizontal').pack(side='top', fill='x')
    # 第三行
    change_line = tk.Frame(master, bg='white')
    tk.Label(change_line, text='更改信息  ID:', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(change_line, textvariable=change_id, width=5, bd=0, font=myFont, bg='lightsteelblue')\
        .pack(side='left', padx=(0, 5))
    tk.Label(change_line, text='要更改的条目:', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    del_tag = ttk.Combobox(change_line, textvariable=change_item, values=['', '药名'], width=10)
    del_tag.current(0)
    del_tag.pack(side='left', padx=(10, 0))
    tk.Label(change_line, text='更改为:', bg='white', font=('song ti', 13)).pack(side='left', padx=(10, 0))
    tk.Entry(change_line, textvariable=change_info, width=15, bd=0, font=myFont, bg='lightsteelblue')\
        .pack(side='left', padx=(0, 5))
    tk.Button(change_line, text='更改', font=('song ti', 13), bd=2, command=change_medicine, fg="#F6FDFE", bg='#4ABD97') \
        .pack(side='left')
    change_line.pack(fill='x', side='top', pady=5)

    ttk.Separator(master, orient='horizontal').pack(side='top', fill='x')
    tree.pack(side='left', fill='x', expand=1)
    ys.pack(side='right', fill='y', anchor='w')
    tree_and_scrollbar.pack(side='top', fill='x', expand=1)


if __name__ == '__main__':
    root = tk.Tk()