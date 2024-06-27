import unittest
import os
import sys
# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件所在目录
current_directory = os.path.dirname(current_file_path)

# 获取上级目录
parent_directory = os.path.dirname(current_directory)

# 添加上级目录到sys.path
sys.path.append(parent_directory)
from sql_handler.handler import handler

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 初始化数据库连接和测试数据
        cls.handler = handler()
        cls.handler.connect_sql_from_config()

    def test_1_add_medicine(self):
        # 测试添加药品和查询功能
        self.handler.test_prepare(500, 'medicine')
        self.handler.add_medicine('500', '测试药品A')
        result = self.handler.select_information_by_id('500', 'medicine')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], '测试药品A')

    # def test_2_delete_medicine(self):
    #     # 测试删除药品功能
    #     self.handler.del_medicine('500', '测试药品A')
    #     result = self.handler.select_information_by_id('500', 'medicine')
    #     self.assertEqual(len(result), 0)

    def test_3_add_supplier(self):
        # 测试添加供应商和从该供应商进货药品功能
        self.handler.test_prepare(101, 'supplier')
        self.handler.add_supplier(101, '测试供应商A', '1234567890', '某地某处')
    
    # def test_4_delete_supplier(self):
    #     # 测试添加供应商和从该供应商进货药品功能
    #     self.handler.del_supplier(101, '测试供应商A', '1234567890', '某地某处')

    def test_5_purchase_from_supplier(self):
        # 测试从已添加的供应商处进货药品
        medicine_id = '500'  # 使用已添加的药品ID
        warehouse_id = '1'  
        supplier_id = 101  # 使用已添加的供应商ID
        stock_id = '111'  # 假设是一个新的进货记录ID

        # 进货数量、价格和日期
        num_in_stock = 20  # 进货数量
        price = 50.00  # 进货价格
        date = '2023-03-01'  # 进货日期

        # 执行进货操作
        result = self.handler.insert_into_stock(stock_id, medicine_id, warehouse_id, supplier_id, num_in_stock, price, date[:4], date[5:7], date[8:])
        print(f"insert_into_stock 返回值: {result}")  # 打印返回值

        self.assertTrue(result == 'True', "进货操作失败")  # 断言返回值是否为 True

        # 验证库房是否有新的药品数量（此处假定已经在库房）
        warehouse_info = self.handler.select_warehouse_all()
        print(f"库房信息: {warehouse_info}")  # 打印库房信息

        is_medicine_in_warehouse = any(warehouse_id == str(info[0]) and 
                                        medicine_id == str(info[1]) for info in warehouse_info)

        self.assertTrue(is_medicine_in_warehouse, "库房中未找到进货的药品")

        # 清理测试数据
        self.handler.del_medicine(medicine_id, None)  # 假设可以通过ID删除药品
  

    

    @classmethod
    def tearDownClass(cls):
        # 清理测试数据和关闭数据库连接
        pass

if __name__ == '__main__':
    unittest.main()
