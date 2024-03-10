import unittest
import sqlite3
import basedata_helper.bd_helper
import basedata_helper.bd_errors


class TestBDHelper(unittest.TestCase):
    def __init__(self, method_name):
        super().__init__(method_name)
        self.bd = sqlite3.connect("basedata_test.db")

    def test_get_value(self):
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_value(
            self.bd, "users"),
            [
                (1, 'admin', 'admin', 2),
                (2, 'Veji', '12345678', 2),
                (3, 'Nickolay', '1234', 1),
                (4, 'Shelby', 'qwer', 1),
                (5, 'Tomas', '13579', 0),
                (6, 'Name', 'SuperSecretPSW', 0)
            ],
            "Get all values from table"
        )
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_value(
            self.bd, "users", ["username"]),
            [('admin',), ('Veji',), ('Nickolay',), ('Shelby',), ('Tomas',), ('Name',)],
            "Get one key from all table values"
        )
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_value(
            self.bd, "users", None, {"username": 'Veji'}),
            [(2, 'Veji', '12345678', 2)],
            "Get all elements from condition"
        )
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_value(
            self.bd, "users", None, {"username": 'Veji', "password": '12345678'}),
            [(2, 'Veji', '12345678', 2)],
            "Get all elements from two conditions "
        )
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_value(
            self.bd, "users", None, {"username": 'Shelby', "password": 'qwer'}, one_element=True),
            (4, 'Shelby', 'qwer', 1),
            "Get one element from condition "
        )

    def test_get_count(self):
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_page_count(
            self.bd, "chapters", f"id_work = Mand", 2), 0)
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_page_count(
            self.bd, "chapters", f"id_work = Mandy", 0), 0)
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_page_count(
            self.bd, "chapters", f"id_work = Mandy", -1), 1)
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_page_count(
            self.bd, "chapters", f"id_work = Mandy", 2), 2)
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_page_count(
            self.bd, "chapters", f"id_work = Mandy", 3), 2)
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_page_count(
            self.bd, "chapters", f"id_work = Mandy", 4), 1)
        self.assertEqual(basedata_helper.bd_helper.BDHelper.get_page_count(
            self.bd, "chapters", f"id_work = Mandy", 1), 4)


if __name__ == '__main__':
    bd = sqlite3.connect("basedata_test.db")
    print(basedata_helper.bd_helper.BDHelper.get_value(
            bd, "users", ["username"]))
    # unittest.main()
