import pymysql as sql
import sql_handler.config as cf


class handler:
    def __init__(self):
        self.connect = None
        self.cursor = None

    def select_all(self, table):
        self.cursor.execute("select * from {}".format(table))
        t = self.cursor.fetchall()
        return t

    def select_information_by_id(self, id_, table):
        self.cursor.execute("select * from {} where {}_id = %s".format(table, table), (id_))
        t = self.cursor.fetchall()
        return t
    
    def select_information_by_id2(self, id_, table):
        try:
            self.cursor.execute("select * from {} where {}_id = %s".format(table, table), (id_))
            t = self.cursor.fetchall()
            return t
        except sql.Error:
            return 'ERROR'
    
    def select_information_by_name(self, name, table):
        self.cursor.execute("select * from {} where name = %s".format(table), (name))
        t = self.cursor.fetchall()
        return t

    def add_medicine(self, medicine_id, name):
        try:
            self.cursor.execute("insert into medicine values(%s, %s)",(medicine_id, name))
            self.connect.commit()
            return True
        except sql.Error as e:
            print(e.args[1])
            return False

    def del_medicine(self, medicine_id, name):
        try:
            self.cursor.execute("delete from medicine where medicine_id = %s or name = %s",(medicine_id, name))
            self.connect.commit()
            return True
        except sql.Error as e:
            print(e.args[1])
            return False

    def change_table(self, id_, name, item, table):
        try:
            self.cursor.execute("update {} set {} = %s where {}_id = %s".format(table, item, table),\
                                (name, id_))
            self.connect.commit()
            return True
        except sql.Error as e:
            print(e.args[1])
            return False

    def add_employee(self, eid, name, poi, phone, passw):
        try:
            self.cursor.execute("insert into employee values(%s, %s, %s, %s, %s)",(eid, name, poi, phone, passw))
            self.connect.commit()
            return True
        except sql.Error as e:
            print(e.args[1])
            return False

    def del_employee(self, eid, name, poi, phone, passw):
        try:
            query = "delete from employee where "
            conditions = []
            params = []
            if eid:
                conditions.append("employee_id = %s")
                params.append(eid)
            if name:
                conditions.append("name = %s")
                params.append(name)
            if poi:
                conditions.append("poisition = %s")
                params.append(poi)
            if phone:
                conditions.append("phone_number = %s")
                params.append(phone)
            if passw:
                conditions.append("passw = %s")
                params.append(passw)
            query += " and ".join(conditions)
            self.cursor.execute(query, tuple(params))
            self.connect.commit()
            return True
        except sql.Error as e:
            print(e.args[1])
            return False

    def add_customer(self, cid, name, phone):
        try:
            self.cursor.execute("insert into customer values(%s, %s, %s)",(cid, name, phone))
            self.connect.commit()
            return True
        except sql.Error as e:
            print(e.args[1])
            return False

    def del_customer(self, cid, name, phone):
        try:
            query = "delete from customer where "
            conditions = []
            params = []
            if cid:
                conditions.append("customer_id = %s")
                params.append(cid)
            if name:
                conditions.append("name = %s")
                params.append(name)
            if phone:
                conditions.append("phone_number = %s")
                params.append(phone)
            query += " and ".join(conditions)
            self.cursor.execute(query, tuple(params))
            self.connect.commit()
            return True
        except sql.Error as e:
            print(e.args[1])
            return False

    def add_supplier(self, sid, name, phone, addr):
        try:
            self.cursor.execute("insert into supplier values(%s, %s, %s, %s)",(sid, name, phone, addr))
            self.connect.commit()
            return True
        except sql.Error as e:
            print(e.args[1])
            return False

    def del_supplier(self, sid, name, phone, addr):
        try:
            query = "delete from supplier where "
            conditions = []
            params = []
            if sid:
                conditions.append("supplier_id = %s")
                params.append(sid)
            if name:
                conditions.append("name = %s")
                params.append(name)
            if phone:
                conditions.append("phone_number = %s")
                params.append(phone)
            if addr:
                conditions.append("address = %s")
                params.append(addr)
            query += " and ".join(conditions)
            self.cursor.execute(query, tuple(params))
            self.connect.commit()
            return True
        except sql.Error as e:
            print(e.args[1])
            return False

    def insert_into_stock(self, _stock_id, _medicine_id, _warehouse_id,_supplier_id,_num,_price,_year,_month,_day):
        ret1 = self.select_information_by_id2(_medicine_id,'medicine')
        if len(ret1)==0:
            return 'medicine_id not found.'
        ret2 = self.select_information_by_id2(_warehouse_id,'warehouse')
        if len(ret2)==0:
            return 'warehouse_id not found.'
        ret3 = self.select_information_by_id2(_supplier_id,'supplier')
        if len(ret3)==0:
            return 'supplier_id not found.'
        try:
            sql_ = f"insert into stock (stock_id,num,price,date_) values({_stock_id},{_num},{_price},'{_year}-{_month}-{_day}')"
            self.cursor.execute(sql_)
            self.connect.commit()
            sql_ = f"insert into medicine_stock (medicine_id,stock_id) values({_medicine_id},{_stock_id})"
            self.cursor.execute(sql_)
            self.connect.commit()
            sql_ = f"insert into supply (supplier_id,stock_id) values({_supplier_id},{_stock_id})"
            self.cursor.execute(sql_)
            self.connect.commit()
            sql_ = f"insert into warehouse_stock (warehouse_id,stock_id) values({_warehouse_id},{_stock_id})"
            self.cursor.execute(sql_)
            self.connect.commit()
            ret =self.select_num_from_store(_medicine_id,_warehouse_id)
            print(ret)
            if ret=='False':
                print('insert')
                sql_ = f"insert into store (medicine_id,warehouse_id,num) value({_medicine_id},{_warehouse_id},{_num})"
                self.cursor.execute(sql_)
                self.connect.commit()
            else :
                print(int(ret)+int(_num))
                sql_ = f"update store set num={int(ret)+int(_num)} where medicine_id={_medicine_id} and warehouse_id={_warehouse_id}"
                self.cursor.execute(sql_)
                self.connect.commit()
            return 'True'
        except sql.Error as e:
            print(e.args[1])
            return e.args[1]

    def insert_into_order(self, _order_id, _medicine_id, _warehouse_id,_customer_id,_employee_id,_num,_price,_type,_year,_month,_day):
        ret1 = self.select_information_by_id2(_medicine_id,'medicine')
        if len(ret1)==0:
            return 'medicine_id not found.'
        ret2 = self.select_information_by_id2(_warehouse_id,'warehouse')
        if len(ret2)==0:
            return 'warehouse_id not found.'
        ret3 = self.select_information_by_id2(_customer_id,'customer')
        if len(ret3)==0:
            return 'customer_id not found.'
        ret4 = self.select_information_by_id2(_employee_id,'employee')
        if len(ret4)==0:
            return 'employee_id not found.'
        
        ret =self.select_num_from_store(_medicine_id,_warehouse_id)
        if ret=='False':
            return 'medicine_id and warehouse_id are not matched.'
        else:
            currentsum = ret
        if _type=='return':
            try:
                sql_ = f"insert into order_table (order_id,num,price,type_,date_) values({_order_id},{_num},{_price},'{_type}','{_year}-{_month}-{_day}')"
                self.cursor.execute(sql_)
                self.connect.commit()
                sql_ = f"insert into medicine_order (medicine_id,order_id) values({_medicine_id},{_order_id})"
                self.cursor.execute(sql_)
                self.connect.commit()
                sql_ = f"insert into place (customer_id,order_id) values({_customer_id},{_order_id})"
                self.cursor.execute(sql_)
                self.connect.commit()
                sql_ = f"insert into process (employee_id,order_id) values({_employee_id},{_order_id})"
                self.cursor.execute(sql_)
                self.connect.commit()
                sql_ = f"insert into warehouse_order (warehouse_id,order_id) values({_warehouse_id},{_order_id})"
                self.cursor.execute(sql_)
                self.connect.commit()
                sql_ = f"update store set num={int(currentsum)+int(_num)} where medicine_id={_medicine_id} and warehouse_id={_warehouse_id}"
                self.cursor.execute(sql_)
                self.connect.commit()
                return 'True'
            except sql.Error as e:
                print(e.args[1])
                return e.args[1]
        elif _type=='sale' and int(_num)>int(currentsum):
            return 'medicine is not enough.'
        else:
            try:
                sql_ = f"insert into order_table (order_id,num,price,type_,date_) values({_order_id},{_num},{_price},'{_type}','{_year}-{_month}-{_day}')"
                self.cursor.execute(sql_)
                self.connect.commit()
                sql_ = f"insert into medicine_order (medicine_id,order_id) values({_medicine_id},{_order_id})"
                self.cursor.execute(sql_)
                self.connect.commit()
                sql_ = f"insert into place (customer_id,order_id) values({_customer_id},{_order_id})"
                self.cursor.execute(sql_)
                self.connect.commit()
                sql_ = f"insert into process (employee_id,order_id) values({_employee_id},{_order_id})"
                self.cursor.execute(sql_)
                self.connect.commit()
                sql_ = f"insert into warehouse_order (warehouse_id,order_id) values({_warehouse_id},{_order_id})"
                self.cursor.execute(sql_)
                self.connect.commit()
                sql_ = f"update store set num={int(currentsum)-int(_num)} where medicine_id={_medicine_id} and warehouse_id={_warehouse_id}"
                self.cursor.execute(sql_)
                self.connect.commit()
                return 'True'
            except sql.Error as e:
                print(e.args[1])
                return e.args[1]

    def select_num_from_store(self,_medicine_id,_warehouse_id):
        try:
            sql_ = f"select num from store where medicine_id={_medicine_id} and warehouse_id={_warehouse_id}"
            self.cursor.execute(sql_)
            t = self.cursor.fetchall()
            if len(t)==0:
                return 'False'
            else:
                print(t[0][0])
                return t[0][0]
        except sql.Error:
            return 'ERROR'

    def select_stock_all(self):
        self.cursor.execute("select stock_id, medicine_id, warehouse_id,supplier_id,num,price,date_ "\
                            "from stock natural join medicine_stock natural join supply natural join warehouse_stock")
        t = self.cursor.fetchall()
        return t

    def select_stock_by_id(self, id):
        sql_ = "select stock_id, medicine_id, warehouse_id,supplier_id,num,price,date_ "\
                    "from stock natural join medicine_stock natural join supply natural join warehouse_stock "\
                    f"where stock_id={id}"
        print(sql_)
        self.cursor.execute(sql_)
        t = self.cursor.fetchall()
        return [[t[0][0], t[0][1], t[0][2], t[0][3], t[0][4], t[0][5], t[0][6]]]
    
    def select_order_all(self):
        self.cursor.execute("select order_id, medicine_id, warehouse_id,customer_id,employee_id,num,price,type_,date_ "\
                            "from order_table natural join medicine_order natural join warehouse_order natural join place natural join process")
        t = self.cursor.fetchall()
        return t

    def select_order_by_id(self, id):
        sql_ = "select order_id, medicine_id, warehouse_id,customer_id,employee_id,num,price,type_,date_ "\
                    "from order_table natural join medicine_order natural join warehouse_order natural join place natural join process "\
                    f"where order_id={id}"
        print(sql_)
        self.cursor.execute(sql_)
        t = self.cursor.fetchall()
        return [[t[0][0], t[0][1], t[0][2], t[0][3], t[0][4], t[0][5], t[0][6], t[0][7], t[0][8]]]

    def select_warehouse_all(self):
        self.cursor.execute("select warehouse_id, medicine_id, name, num from medicine natural join store")
        t = self.cursor.fetchall()
        return t

    def select_warehouse_information_by_id(self, id_):
        self.cursor.execute("select warehouse_id, medicine_id, name, num from medicine natural join store where medicine_id=%s", (id_))
        t = self.cursor.fetchall()
        return t
    
    def select_warehouse_information_by_name(self, name):
        self.cursor.execute("select warehouse_id, medicine_id, name, num from medicine natural join store where name=%s", (name))
        t = self.cursor.fetchall()
        return t

    def insert_warehouse(self, id_, addr):
        self.cursor.execute("insert into warehouse values(%s, %s)", (id_, addr))


    def connect_sql_from_config(self):
        self.connect = sql.connect(host=cf.host,
                                   user=cf.username,
                                   password=cf.password,
                                   database=cf.database,
                                   autocommit=True,
                                   charset=cf.charset)
        self.cursor = self.connect.cursor()

    def connect_sql(self, user, pwd):
        self.connect = sql.connect(host=cf.host,
                                   user=user,
                                   password=pwd,
                                   database=cf.database,
                                   autocommit=True,
                                   charset=cf.charset)
        self.cursor = self.connect.cursor()


    # 查询某日收入情况
    def select_income_by_date(self, currDate):
        sql_ = f"select medicine_id, medicine.name, " \
               f"sum(stock_report.total_num), sum(stock_report.total_price), " \
               f"sum(sales_report.total_num), sum(stock_report.total_price) " \
               f"from stock_report natural join medicine natural join sales_report " \
               f"where stock_report.date_ ='{currDate}' " \
               f"group by medicine_id, medicine.name;"
        print(sql_)
        self.cursor.execute(sql_)
        return self.cursor.fetchall()

    def select_stock_by_date(self, currDate):
        sql_ = f"select medicine_id, medicine.name, " \
               f"sum(stock_report.total_num), sum(stock_report.total_price) " \
               f"from stock_report natural join medicine " \
               f"where stock_report.date_ ='{currDate}' " \
               f"group by medicine_id, medicine.name;"
        print(sql_)
        self.cursor.execute(sql_)
        return self.cursor.fetchall()
    
    def select_sales_by_date(self, currDate):
        sql_ = f"select medicine_id, medicine.name, " \
               f"sum(sales_report.total_num), sum(sales_report.total_price) " \
               f"from sales_report natural join medicine " \
               f"where sales_report.date_ ='{currDate}' " \
               f"group by medicine_id, medicine.name;"
        print(sql_)
        self.cursor.execute(sql_)
        return self.cursor.fetchall()

    def select_warehouse_for_report(self):
        sql_ = f"select warehouse_id, warehouse.address " \
               f"medicine_id, medicine.name, store.num " \
               f"from medicine natural join store natural join warehouse"
        print(sql_)
        self.cursor.execute(sql_)
        return self.cursor.fetchall()    


    # 查询某月收入情况
    def select_income_by_month(self, year, month):
        sql_ = f"select medicine_id, medicine.name, " \
               f"sum(stock_report.total_num), sum(stock_report.total_price), " \
               f"sum(sales_report.total_num), sum(stock_report.total_price) " \
               f"from stock_report natural join medicine natural join sales_report " \
                f"where year(stock_report.date_) = '{year}' and month(stock_report.date_) = '{month}' " \
               f"group by medicine_id, medicine.name;"
        print(sql_)
        self.cursor.execute(sql_)
        return self.cursor.fetchall()

    def select_stock_by_month(self, year, month):
        sql_ = f"select medicine_id, medicine.name, " \
               f"sum(stock_report.total_num), sum(stock_report.total_price) " \
               f"from stock_report natural join medicine " \
                f"where year(stock_report.date_) = '{year}' and month(stock_report.date_) = '{month}' " \
               f"group by medicine_id, medicine.name;"
        print(sql_)
        self.cursor.execute(sql_)
        return self.cursor.fetchall()
    
    def select_sales_by_month(self, year, month):
        sql_ = f"select medicine_id, medicine.name, " \
               f"sum(sales_report.total_num), sum(sales_report.total_price) " \
               f"from sales_report natural join medicine " \
                f"where year(sales_report.date_) = '{year}' and month(sales_report.date_) = '{month}' " \
               f"group by medicine_id, medicine.name;"
        print(sql_)
        self.cursor.execute(sql_)
        return self.cursor.fetchall()

    # 查询某年收入情况
    def select_income_by_year(self, year):
        sql_ = f"select medicine_id, medicine.name, " \
               f"sum(stock_report.total_num), sum(stock_report.total_price), " \
               f"sum(sales_report.total_num), sum(stock_report.total_price) " \
               f"from stock_report natural join medicine natural join sales_report " \
               f"where year(stock_report.date_) = '{year}'" \
               f"group by medicine_id, medicine.name;"

        print(sql_)
        self.cursor.execute(sql_)
        return self.cursor.fetchall()

    def select_stock_by_year(self, year):
        sql_ = f"select medicine_id, medicine.name, " \
               f"sum(stock_report.total_num), sum(stock_report.total_price) " \
               f"from stock_report natural join medicine " \
               f"where year(stock_report.date_) = '{year}'" \
               f"group by medicine_id, medicine.name;"

        print(sql_)
        self.cursor.execute(sql_)
        return self.cursor.fetchall()

    def select_sales_by_year(self, year):
        sql_ = f"select medicine_id, medicine.name, " \
               f"sum(sales_report.total_num), sum(sales_report.total_price) " \
               f"from sales_report natural join medicine " \
               f"where year(sales_report.date_) = '{year}'" \
               f"group by medicine_id, medicine.name;"

        print(sql_)
        self.cursor.execute(sql_)
        return self.cursor.fetchall()

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()  # 先关闭游标
        if self.cursor is not None:
            self.connect.close()  # 再关闭数据库连接
    
