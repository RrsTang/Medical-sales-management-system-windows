import tkinter as tk
import sys
import os

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件所在目录
current_directory = os.path.dirname(current_file_path)

# 获取上级目录
parent_directory = os.path.dirname(current_directory)

# 添加上级目录到sys.path
sys.path.append(parent_directory)

from sql_handler.handler import *  # sql 接口
from sql_handler.config import *  # sql 配置文件
from tkinter import messagebox  # tkinter 弹窗
from gui.login import login_page
from gui.normal_page import normal_page
from gui.head_info import head_handle
from gui.report import *

from gui.base_info import base_info
from gui.medicine_info import medicine_info
from gui.employee_info import employee_info
from gui.customer_info import customer_info
from gui.supplier_info import supplier_info
from gui.warehouse import warehouse

from gui.stock import stoke_page
from gui.sales import sales_page

class MainUI:
    def __init__(self):
        # 窗口参数
        self.window = tk.Tk()
        self.window.title('医药销售管理系统')
        self.window.maxsize(2000, 700)
        self.window.minsize(1050, 700)
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        # self.window.config(encoding='utf-8')

        # 登录界面参数
        self.usr_name = tk.StringVar()
        self.usr_pwd = tk.StringVar()
        self.current_operator = None
        print(self.usr_name)
        print(self.usr_pwd)

        # -------开发参数！！！ 记得删除-----------------------------
        self.usr_name.set(username)
        self.usr_pwd.set(password)
        # -----------------------------------------------------

        # 主界面参数
        self.normal_mode = tk.StringVar()
        self.base_info_mode = tk.StringVar()

        self.hd = handler()
        # （页面）框架列表
        self.login_page = None  # 登录页面
        self.normal_page = None  # 主页面
        self.head_info = None  # 头注
        self.foot_info = None  # 脚注

        self.report_main_page = None # 报表系统主页面
        self.report_mode = tk.StringVar()  # 报表系统模式
        self.report_finance = None  # 财报系统
        self.report_stock = None  # 入库信息
        self.report_sales = None  # 销售信息
        self.report_warehouse = None  # 仓库信息

        self.base_info = None
        self.medicine_info = None
        self.employee_info = None
        self.customer_info = None
        self.applier_info = None
        self.warehouse = None

        # 进货
        self.stock = None
        # 销售
        self.sales =None

        # 开始渲染 login 页面
        self.get_login()

    # 获取 login 页面
    def get_login(self):
        self.login_page = tk.Frame(self.window, bg='white')
        login_page(self.login_page, self.usr_name, self.usr_pwd, self.login_handle)
        self.login_page.pack(fill='both')

    # 获取主页面
    def get_normal(self):
        # self.window.geometry('970x600+200+30')
        self.normal_page = tk.Frame(self.window, bg='#ffffff')
        normal_page(self.normal_page, self.normal_mode, self.hd, self.normal_handle)
        self.normal_page.pack(fill='both')

    # 获取头部信息和脚注
    def get_headinfo(self):
        self.head_info = tk.Frame(self.window)
        head_handle(self.head_info, self.usr_name.get())
        self.head_info.pack(side='top', fill='both')

    def getin_base_info(self):
        self.base_info = tk.Frame(self.window, bg='#F0F0F0')
        base_info(self.base_info, self.base_info_mode, self.hd, self.base_info_handle)
        self.base_info.pack(fill='both')

    def getin_medicine_info(self):
        self.medicine_info = tk.Frame(self.window, bg='#F0F0F0')
        medicine_info(self.medicine_info, self.getin_base_info, self.hd)
        self.medicine_info.pack(fill='both')

    def getin_employee_info(self):
        self.employee_info = tk.Frame(self.window, bg='#F0F0F0')
        employee_info(self.employee_info, self.getin_base_info, self.hd, self.curr_operator)
        self.employee_info.pack(fill='both')

    def getin_customer_info(self):
        self.customer_info = tk.Frame(self.window, bg='#F0F0F0')
        customer_info(self.customer_info, self.getin_base_info, self.hd)
        self.customer_info.pack(fill='both')

    def getin_applier_info(self):
        self.applier_info = tk.Frame(self.window, bg='#F0F0F0')
        supplier_info(self.applier_info, self.getin_base_info, self.hd)
        self.applier_info.pack(fill='both')

    def getin_warehouse(self):
        self.warehouse = tk.Frame(self.window, bg='#F0F0F0')
        warehouse(self.warehouse, self.get_normal, self.hd)
        self.warehouse.pack(fill='both')

    # 获取进货管理页面
    def get_stock(self):
        self.stock = tk.Frame(self.window, bg='white')
        stoke_page(self.stock, self.get_normal, self.hd)
        self.stock.pack(fill='both')

    # 获取销售管理页面
    def get_sales(self):
        self.sales = tk.Frame(self.window, bg='white')
        sales_page(self.sales, self.get_normal, self.hd)
        self.sales.pack(fill='both')

    # 登录页面响应接口
    def login_handle(self, event=None):
        name = self.usr_name.get()
        pwd = self.usr_pwd.get()
        print(name)
        print(pwd)
        try:
            self.hd.connect_sql('root', mysql_server_password)
            if name != 'root' or pwd != 'root':
                pass_ = self.hd.select_all('employee')
                for item in pass_:
                    n = str(item[0])
                    p = str(item[4])
                    print(n, p)
                    if name == n and pwd == p:
                        self.curr_operator = name
                        break
                else:
                    tk.messagebox.showerror(message='登录失败：请检查用户名和密码。')
                    return
            else:
                self.curr_operator = 'root'
        except Exception as e:
            print(e)
            tk.messagebox.showerror(message='登录失败：请检查用户名和密码。')
            return
        print('log: Successfully connect database.')
        print('loading tables...')
        print('current operator:', self.curr_operator)
        self.window.title('医药销售管理系统(当前操作员：' + self.curr_operator + ')')
        self.hd.execute_script_from_file('sql/sql.txt')
        self.usr_pwd.set("")
        self.login_page.destroy()
        # 渲染员工操作页面
        self.get_headinfo()
        self.get_normal()

    # 主页面响应接口
    def normal_handle(self):
        self.normal_page.destroy()
        mode = self.normal_mode.get()
        if mode == 'exit':
            self.head_info.destroy()
            # self.foot_info.destroy()
            self.get_login()
        elif mode == 'base_info':
            self.getin_base_info()
        elif mode == 'warehouse':
            self.getin_warehouse()
        # stock
        elif mode == 'stock':
            self.get_stock()
        # sales
        elif mode == 'sales':
            self.get_sales()
        else:  # model == 'report'
            self.get_report_main()

    # 获取报表系统主页面
    def get_report_main(self):
        # self.window.geometry('970x600+200+30')
        self.report_main_page = tk.Frame(self.window, bg='#F0F0F0')
        report_main_page(self.report_main_page, self.report_mode, self.hd, self.report_main_handle)
        self.report_main_page.pack(fill='both')
    
    # 获取报表系统-财务报表
    def report_finance_info(self):
        # print('get financial info')
        self.report_finance = tk.Frame(self.window, bg='white')
        report_finance_page(self.report_finance, self.get_report_main, self.hd)
        self.report_finance.pack(fill='both')

    # 获取报表系统-入库报表
    def report_stock_info(self):
        self.report_stock = tk.Frame(self.window, bg='white')
        report_stock_page(self.report_stock, self.get_report_main, self.hd)
        self.report_stock.pack(fill='both')
    
    # 获取报表系统-销售报表
    def report_sales_info(self):
        self.report_sales = tk.Frame(self.window, bg='white')
        report_sales_page(self.report_sales, self.get_report_main, self.hd)
        self.report_sales.pack(fill='both')
    
    # 获取报表系统-仓库报表
    def report_warehouse_info(self):
        self.report_warehouse = tk.Frame(self.window, bg='white')
        report_warehouse_page(self.report_warehouse, self.get_report_main, self.hd)
        self.report_warehouse.pack(fill='both')

    def report_main_handle(self):
        self.report_main_page.destroy()
        mode = self.report_mode.get()
        print (f'Current mode is {mode}.')
        if mode == 'financial':
            self.report_finance_info()
        elif mode == 'stock':
            self.report_stock_info()
        elif mode == 'sales':
            self.report_sales_info()
        elif mode == 'warehouse':
            self.report_warehouse_info()
        else:  # mode == 'exit'
            self.get_normal()

    def base_info_handle(self):
        self.base_info.destroy()
        mode = self.base_info_mode.get()
        if mode == 'medicine':
            self.getin_medicine_info()
        elif mode == 'employee':
            self.getin_employee_info()
        elif mode == 'customer':
            self.getin_customer_info()
        elif mode == 'applier':
            self.getin_applier_info()
        else:
            self.get_normal()

if __name__ == '__main__':
    ui = MainUI()
    ui.window.mainloop()
