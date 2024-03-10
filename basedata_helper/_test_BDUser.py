import sqlite3
import unittest
from bd_user import BDUser


class TestBDHelper(unittest.TestCase):
    def __init__(self, method_name):
        super().__init__(method_name)
        self.bd = sqlite3.connect("basedata_test.db")

    def test_user_authorization(self):
        self.assertEqual(BDUser.check_user_authorization(self.bd, "Shelby", "qwer"),
                         {'id_user': 4, 'permission': 1, 'username': 'Shelby'})
        self.assertEqual(BDUser.check_user_authorization(self.bd, "Shelby", "qwerty"),
                         None)

    def test_is_user_exists_by_his_username(self):
        self.assertEqual(BDUser.is_user_exists_by_his_username(self.bd, "Shelby"), True)
        self.assertEqual(BDUser.is_user_exists_by_his_username(self.bd, "Veji"), True)
        self.assertEqual(BDUser.is_user_exists_by_his_username(self.bd, "veji"), False)
        self.assertEqual(BDUser.is_user_exists_by_his_username(self.bd, "Snejok"), False)

    def test_is_user_exists_by_his_id(self):
        self.assertEqual(BDUser.is_user_exists_by_his_id(self.bd, 4), True)
        self.assertEqual(BDUser.is_user_exists_by_his_id(self.bd, 2), True)
        self.assertEqual(BDUser.is_user_exists_by_his_id(self.bd, 1999), False)
        self.assertEqual(BDUser.is_user_exists_by_his_id(self.bd, 25678), False)

    def test_get_user_info_for_his_id(self):
        self.assertEqual(BDUser.get_user_info_for_his_id(self.bd, 3), {"username": "Nickolay", "permission": 1})
        self.assertEqual(BDUser.get_user_info_for_his_id(self.bd, -8), None)
        self.assertEqual(BDUser.get_user_info_for_his_id(self.bd, 1826), None)
        self.assertEqual(BDUser.get_user_info_for_his_id(self.bd, 5), {"username": "Tomas", "permission": 0})


if __name__ == '__main__':
    unittest.main()
