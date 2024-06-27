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
        self.handler.add_medicine('500', '测试药品A')
        result = self.handler.select_information_by_id('500', 'medicine')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], '测试药品A')

    def test_2_update_medicine_info(self):
        # 测试更新药品信息
        self.handler.change_table('500', '测试药品A_更新', 'name', 'medicine')
        result = self.handler.select_information_by_id('500', 'medicine')
        self.assertEqual(result[0][1], '测试药品A_更新')

    # def test_3_delete_medicine(self):
    #     # 测试删除药品功能
    #     self.handler.del_medicine('500', '测试药品A_更新')
    #     result = self.handler.select_information_by_id('500', 'medicine')
    #     self.assertEqual(len(result), 0)

    @classmethod
    def tearDownClass(cls):
        # 清理测试数据和关闭数据库连接
        pass

if __name__ == '__main__':
    unittest.main()