import unittest
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

from sql_handler.handler import handler 

class TestDatabaseConnection(unittest.TestCase):# 继承自单元测试的基础类unittest.TestCase
    def setUp(self):
        self.db_handler = handler()  # 初始化数据库处理器，创建实例用于处理数据库连接

    def test_database_connection(self):
        try:
            self.db_handler.connect_sql_from_config()  # 使用配置文件中的连接信息连接数据库
            # 断言数据库连接对象不为 None
            self.assertIsNotNone(self.db_handler.connect, "Database connection should not be None.")
            print("Database connection test passed.")
        except Exception as e:
            self.fail(f"Database connection test failed: {str(e)}")
    # 清理资源
    def tearDown(self):
        del self.db_handler  

if __name__ == '__main__':
    unittest.main(argv=sys.argv[:1])
