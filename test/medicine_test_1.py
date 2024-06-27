import unittest
import tkinter as tk
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

from gui.medicine_info import medicine_info
from sql_handler.handler import handler

class TestMedicineCRUDOperations(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.db_handler = handler()
        self.db_handler.connect_sql_from_config() 
        # 在 GUI 中初始化药品信息界面
        medicine_info(self.root, self.root.quit, self.db_handler)
        self.root.update() 

    def test_add_medicine(self):
        # 测试添加药品
        medicine_id = '101'
        medicine_name = 'TestMedicineAdd'
        self.db_handler.test_prepare(medicine_id, 'medicine')
        print("Available widget names:", self.find_widget_names(self.root))
        entry_id = self.find_widget_by_name(self.root, 'entry_medicine_id')
        entry_name = self.find_widget_by_name(self.root, 'entry_medicine_name')
        button_add = self.find_widget_by_name(self.root, 'button_add')

        self.assertIsNotNone(entry_id, "Medicine ID entry not found")
        self.assertIsNotNone(entry_name, "Medicine name entry not found")
        self.assertIsNotNone(button_add, "Add button not found")

        entry_id.delete(0, 'end')
        entry_id.insert(0, medicine_id)
        entry_name.delete(0, 'end')
        entry_name.insert(0, medicine_name)
        button_add.invoke()

        self.root.update_idletasks()
        result = self.db_handler.select_information_by_id(medicine_id, 'medicine')
        self.assertNotEqual(len(result), 0, "添加药品失败")

    def test_delete_medicine(self):
        # 测试删除药品
        medicine_id = '102'
        medicine_name = 'TestMedicineDelete'
        self.db_handler.test_prepare(medicine_id, 'medicine')
        self.db_handler.add_medicine(medicine_id, medicine_name)
        self.root.update()
        entry_id = self.find_widget_by_name(self.root, 'entry_medicine_id')
        entry_name = self.find_widget_by_name(self.root, 'entry_medicine_name')
        button_delete = self.find_widget_by_name(self.root, 'button_delete')

        self.assertIsNotNone(entry_id, "Medicine ID entry not found")
        self.assertIsNotNone(entry_name, "Medicine name entry not found")
        self.assertIsNotNone(button_delete, "Delete button not found")

        entry_id.delete(0, 'end')
        entry_id.insert(0, medicine_id)
        entry_name.delete(0, 'end')
        entry_name.insert(0, medicine_name)
        button_delete.invoke()

        self.root.update_idletasks()
        result = self.db_handler.select_information_by_id(medicine_id, 'medicine')
        self.assertEqual(len(result), 0, "删除药品失败")

    def test_find_medicine_by_id(self):
        # 测试通过ID查询药品
        medicine_id = '103'
        medicine_name = 'TestMedicineFindById'
        self.db_handler.test_prepare(medicine_id, 'medicine')
        self.db_handler.add_medicine(medicine_id, medicine_name)
        self.root.update()
        entry_id = self.find_widget_by_name(self.root, 'entry_medicine_id')
        button_query = self.find_widget_by_name(self.root, '!button')

        self.assertIsNotNone(entry_id, "Medicine ID entry not found")
        self.assertIsNotNone(button_query, "Query button not found")

        entry_id.delete(0, 'end')
        entry_id.insert(0, medicine_id)
        button_query.invoke()

        self.root.update_idletasks()
        tree = self.find_widget_by_name(self.root, '!treeview')
        items = tree.get_children()
        found = False
        for item in items:
            values = tree.item(item, "values")
            if values[0] == medicine_id and values[1] == medicine_name:
                found = True
                break
        self.assertTrue(found, "未找到药品")

    def test_update_medicine(self):
        # 测试修改药品信息
        medicine_id = '104'
        old_medicine_name = 'TestMedicineUpdate'
        new_medicine_name = 'TestMedicineUpdated'
        self.db_handler.test_prepare(medicine_id, 'medicine')
        self.db_handler.add_medicine(medicine_id, old_medicine_name)
        self.root.update()
        change_id = self.find_widget_by_name(self.root, 'entry_change_id')
        change_info = self.find_widget_by_name(self.root, 'entry_change_info')
        change_item = self.find_widget_by_name(self.root, 'combobox_change_item')
        button_change = self.find_widget_by_name(self.root, 'button_change')

        self.assertIsNotNone(change_id, "Change ID entry not found")
        self.assertIsNotNone(change_info, "Change info entry not found")
        self.assertIsNotNone(change_item, "Change item combobox not found")
        self.assertIsNotNone(button_change, "Change button not found")

        change_id.delete(0, 'end')
        change_id.insert(0, medicine_id)
        change_info.delete(0, 'end')
        change_info.insert(0, new_medicine_name)
        change_item.set('药名')
        button_change.invoke()

        self.root.update_idletasks()
        result = self.db_handler.select_information_by_id(medicine_id, 'medicine')
        print(result)
        self.assertEqual(result[0][1], new_medicine_name, "修改药品失败")

    def tearDown(self):
        self.root.destroy()
        del self.db_handler

    def find_widget_by_name(self, widget, name):
        if widget.winfo_name() == name:
            return widget
        for child in widget.winfo_children():
            result = self.find_widget_by_name(child, name)
            if result is not None:
                return result
        return None

    def find_widget_names(self, widget):
        names = []
        for child in widget.winfo_children():
            names.append(child.winfo_name())
            names.extend(self.find_widget_names(child))
        return names

if __name__ == '__main__':
    unittest.main()