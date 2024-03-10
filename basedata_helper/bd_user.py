import pprint
import sqlite3
import basedata_helper.bd_helper
import basedata_helper.bd_unit


class BDUser(basedata_helper.bd_unit.BDUnit):
    TABLE_NAME = "users"
    PRIMARY_KEYS = ["id_user"]
    KEYS = ["id_user", "username", "password", "permission"]

    @classmethod
    def is_user_exists_by_his_username(cls, bd_connection: sqlite3.Connection, username: str) -> bool:
        data = basedata_helper.bd_helper.BDHelper.get_value(
            bd_connection,
            cls.TABLE_NAME, None, {"username": username})
        if data:
            return len(data) > 0
        return False

    @classmethod
    def is_user_exists_by_his_id(cls, bd_connection: sqlite3.Connection, id_user: int) -> bool:
        data = basedata_helper.bd_helper.BDHelper.get_value(
            bd_connection,
            cls.TABLE_NAME, None, {"id_user": id_user})
        if data:
            return len(data) > 0
        return False

    @classmethod
    def check_user_authorization(cls, bd_connection: sqlite3.Connection, username: str, password: str):
        data = basedata_helper.bd_helper.BDHelper.get_value(
            bd_connection,
            cls.TABLE_NAME, None, {"username": username, "password": password},
            one_element=True)
        if data:
            return {
                "id_user": data[0],
                "username": data[1],
                "permission": data[3]
            }
        return None

    @classmethod
    def get_user_info_for_his_id(cls, bd_connection: sqlite3.Connection, id_user: int):
        data = basedata_helper.bd_helper.BDHelper.get_value(
            bd_connection,
            cls.TABLE_NAME, None, {"id_user": id_user}, one_element=True)
        if data:
            return {
                "id_user": data[0],
                "username": data[1],
                "permission": data[3]
            }
        return None

    @classmethod
    def get_user_info_for_his_username(cls, bd_connection: sqlite3.Connection, username: str):
        data = basedata_helper.bd_helper.BDHelper.get_value(
            bd_connection,
            cls.TABLE_NAME, None, {"username": username}, one_element=True)
        if data:
            return {
                "id_user": data[0],
                "username": data[1],
                "permission": data[3]
            }
        return None

    @classmethod
    def user_registration(cls, bd_connection: sqlite3.Connection, username: str, password: str, permission: int = 0):
        if cls.is_user_exists_by_his_username(bd_connection, username):
            return None
        data = cls.append_item(bd_connection, {"username": username, "password": password, "permission": permission})
        print(data)
        if data:
            return {
                "id_user": data["id_user"],
                "username": data["username"],
                "permission": data["permission"]
            }
        return None


if __name__ == "__main__":
    bd = sqlite3.connect("basedata_test.db")
    print("\n", "=" * 3, "---   Test BDUser.get_all()   ---", "=" * 3, sep="")
    pprint.pprint(BDUser.get_all(bd))
    print("\n", "=" * 3, "---   Test BDUser.is_user_exists_by_his_id()   ---", "=" * 3, sep="")
    pprint.pprint(BDUser.is_user_exists_by_his_id(bd, 1))
    print("\n", "=" * 3, "---   Test BDUser.is_user_exists_by_his_username()   ---", "=" * 3, sep="")
    pprint.pprint(BDUser.is_user_exists_by_his_username(bd, "Shelby"))
    print("\n", "=" * 3, "---   Test BDUser.check_user_authorization()   ---", "=" * 3, sep="")
    pprint.pprint(BDUser.check_user_authorization(bd, "Shelby", "qwer"))
    print("\n", "=" * 3, "---   Test BDUser.get_user_info_for_his_id()   ---", "=" * 3, sep="")
    pprint.pprint(BDUser.get_user_info_for_his_id(bd, 4))
