from flask import g
import os.path
import sqlite3
import logging
import basedata_helper.bd_errors
import basedata_helper.sql_helper



class BDHelper:
    BD_TYPE = "SQLite"
    BD_TYPES = ["SQLite"]
    BD_FILE = "basedata_test.db"
    BD_PATH_TO_FILES = ''

    @classmethod
    def init(cls, bd_type: str, bd_name: str, path_to_files: str = None):
        cls.BD_TYPE = bd_type
        cls.BD_FILE = bd_name
        cls.BD_PATH_TO_FILES = '' if path_to_files is None else path_to_files
        print(os.getcwd())

    @classmethod
    def init_from_file(cls, file_name: str):
        bd_type = None
        bd_file = None
        bd_path_to_files = None
        init_file = open(file_name, "r")
        lines = init_file.readlines()
        for line in lines:
            buffer = line.replace(' ', '', -1)
            buffer = buffer.replace('\t', '', -1)
            buffer = buffer.replace('\n', '', -1)
            if "#" in buffer:
                buffer = buffer[:buffer.find("#")]
            if 'BD_TYPE' in line:
                bd_type = buffer.split(":")[-1]
            if 'BD_FILE' in line:
                bd_file = buffer.split(":")[-1]
            if 'BD_PATH_TO_FILES' in line:
                bd_path_to_files = buffer.split(":")[-1]
        if bd_type is None:
            raise basedata_helper.bd_errors.BDErrorInitFile(f"BD_TYPE field not exists in init file")
        if bd_file is None:
            raise basedata_helper.bd_errors.BDErrorInitFile(f"BD_FILE field not exists in init file")
        if bd_path_to_files is None:
            raise basedata_helper.bd_errors.BDErrorInitFile(f"BD_PATH_TO_FILES field not exists in init file")
        if bd_type not in cls.BD_TYPES:
            raise basedata_helper.bd_errors.BDErrorInitFile(f"BD type = {bd_type} is not exists")
        if not os.path.exists(bd_file):
            raise basedata_helper.bd_errors.BDErrorInitFile(f"BD name = {bd_path_to_files} is not exists")
        if not os.path.isfile(bd_file):
            raise basedata_helper.bd_errors.BDErrorInitFile(f"BD name = {bd_file} is not file")
        if bd_path_to_files != '' and not os.path.exists(bd_path_to_files):
            raise basedata_helper.bd_errors.BDErrorInitFile(f"BD path to files = {bd_path_to_files} is not exists")
        if bd_path_to_files != '' and not os.path.isdir(bd_path_to_files):
            raise basedata_helper.bd_errors.BDErrorInitFile(f"BD path to files = {bd_path_to_files} is not a dir")
        cls.BD_TYPE = bd_type
        cls.BD_FILE = bd_file
        cls.BD_PATH_TO_FILES = bd_path_to_files

    @classmethod
    def get_db(cls):
        if cls.BD_TYPE == "SQLite":
            db = getattr(g, '_database', None)
            if db is None:
                db = g._database = sqlite3.connect(cls.BD_FILE)
            return db

    @staticmethod
    def get_items(
            bd_connection: sqlite3.Connection,
            table_name: str,
            selected_header: list[str] = None,
            condition: str = None,
            limit: int = -1, offset: int = 0,
            sorted_headers: list = None,
            reverse: bool = True
    ):
        selected_header = (", ".join(selected_header) if selected_header is not None else "*")
        if sorted_headers is not None and len(sorted_headers) > 0:
            sorted_headers = "ORDER BY " + ", ".join(sorted_headers) + (" DESC" if reverse else " ASC")
        else:
            sorted_headers = ""
        condition = " WHERE " + condition if condition else ""
        if BDHelper.BD_TYPE == "SQLite":
            sql_command = \
                f"SELECT {selected_header} FROM {table_name}{condition} {sorted_headers} LIMIT {limit} OFFSET {offset};"
            logging.info(
                f"CLASS: BDHelper; Method: get_items; BD_TYPE: {BDHelper.BD_TYPE}; SQL_COMMAND: {sql_command};")
            return basedata_helper.sql_helper.SQLiteHelperBD.execute_all(bd_connection, sql_command)
        return None

    @staticmethod
    def get_item(
            bd_connection: sqlite3.Connection,
            table_name: str, selected_header: list[str] = None, condition: str = None):
        selected_header = (", ".join(selected_header) if selected_header is not None else "*")
        condition = " WHERE " + condition if condition else ""
        if BDHelper.BD_TYPE == "SQLite":
            sql_command = \
                f"SELECT {selected_header} FROM {table_name}{condition};"
            logging.info(
                f"CLASS: BDHelper; Method: get_item; BD_TYPE: {BDHelper.BD_TYPE}; SQL_COMMAND: {sql_command};")
            return basedata_helper.sql_helper.SQLiteHelperBD.execute_one(bd_connection, sql_command)
        return None

    @staticmethod
    def get_value(
            bd_connection: sqlite3.Connection,
            table_name: str,
            selected_header: list[str] = None,
            condition: dict = None,
            or_logic: bool = False,
            one_element: bool = False,
            limit: int = -1, offset: int = 0,
            sorted_headers: list = None,
            reverse: bool = True
    ) -> tuple | None:
        """ SELECT < selected_header_1, selected_header_2... > FROM <table_name> WHERE <condition for get by id>"""
        selected_header = (", ".join(selected_header) if selected_header is not None else "*")
        if sorted_headers is not None and len(sorted_headers) > 0:
            sorted_headers = "ORDER BY " + ", ".join(sorted_headers) + (" DESC" if reverse else " ASC")
        else:
            sorted_headers = ""
        if condition is None:
            condition = ""
        else:
            logic = " OR " if or_logic else " AND "
            condition = " WHERE " + logic.join([f"{key} = '{value}'" for key, value in condition.items()])
        if BDHelper.BD_TYPE == "SQLite":
            sql_command = f"SELECT {selected_header} FROM {table_name}{condition} {sorted_headers} LIMIT {limit} OFFSET {offset};"
            logging.info(
                f"CLASS: BDHelper; Method: get_value; BD_TYPE: {BDHelper.BD_TYPE}; SQL_COMMAND: {sql_command};")
            if one_element:
                return basedata_helper.sql_helper.SQLiteHelperBD.execute_one(bd_connection, sql_command)
            return basedata_helper.sql_helper.SQLiteHelperBD.execute_all(bd_connection, sql_command)
        return None

    @staticmethod
    def get_page_count(
            bd_connection: sqlite3.Connection,
            table_name: str,
            condition: str = None,
            limit: int = -1
    ) -> int:
        if limit == 0:
            return 0
        condition = " WHERE " + condition if condition else ""
        if BDHelper.BD_TYPE == "SQLite":
            sql_command = f"SELECT COUNT(*) FROM {table_name}{condition};"
            logging.info(
                f"CLASS: BDHelper; Method: get_value; BD_TYPE: {BDHelper.BD_TYPE}; SQL_COMMAND: {sql_command};")
            d = basedata_helper.sql_helper.SQLiteHelperBD.execute_one(bd_connection, sql_command)[0]
            if d == 0:
                return 0
            if limit < 0:
                return 1
            if d % limit == 0:
                return d // abs(limit)
            else:
                return d // abs(limit) + 1
        return 0

    @staticmethod
    def del_element(
            bd_connection: sqlite3.Connection,
            table_name: str,
            condition: dict,
            one_element: bool = True,
            values_return: list[str] = None
    ) -> tuple | None:
        if not isinstance(condition, dict):
            return None
        condition = " WHERE " + " AND ".join([f"{key} = '{value}'" for key, value in condition.items()])
        values_return = " * " if values_return is None else ", ".join(values_return)
        if BDHelper.BD_TYPE == "SQLite":
            sql_command = f"DELETE FROM {table_name}{condition} RETURNING {values_return};"
            logging.info(
                f"CLASS: BDHelper; Method: del_element; BD_TYPE: {BDHelper.BD_TYPE}; SQL_COMMAND: {sql_command};")
            if one_element:
                return basedata_helper.sql_helper.SQLiteHelperBD.execute_commit_one(bd_connection, sql_command)
            return basedata_helper.sql_helper.SQLiteHelperBD.execute_commit_all(bd_connection, sql_command)
        return None

    @staticmethod
    def add_element(
            bd_connection: sqlite3.Connection,
            table_name: str,
            added_values: dict,
            values_return: list[str] = None
    ) -> tuple | None:
        headers = f"( {', '.join(added_values.keys())} )"
        added_values = "('" + "', '".join(map(lambda x: str(x), added_values.values())) + "')"
        values_return = " * " if values_return is None else ", ".join(values_return)
        if BDHelper.BD_TYPE == "SQLite":
            sql_command = f"INSERT INTO {table_name} {headers} VALUES {added_values} RETURNING {values_return};"
            try:
                return basedata_helper.sql_helper.SQLiteHelperBD.execute_commit_one(bd_connection, sql_command)
            except sqlite3.IntegrityError:
                raise basedata_helper.bd_errors.BDErrorItemExists(
                    f"Item with values {added_values} exists in table '{table_name}'.")
        return None

    @staticmethod
    def update_element(
            bd_connection: sqlite3.Connection,
            table_name: str,
            updated_values: dict,
            condition: dict
    ) -> None | tuple:
        updated_values = ", ".join(f"{key} = '{value}'" for key, value in updated_values.items())
        condition = " AND ".join([f"{key} = '{value}'" for key, value in condition.items()])
        if BDHelper.BD_TYPE == "SQLite":
            sql_command = f"UPDATE {table_name} SET {updated_values} WHERE {condition} RETURNING *;"
            logging.info(
                f"CLASS: BDHelper; Method: update_element; BD_TYPE: {BDHelper.BD_TYPE}; SQL_COMMAND: {sql_command};")
            return basedata_helper.sql_helper.SQLiteHelperBD.execute_commit_one(bd_connection, sql_command)
        return None


if __name__ == "__main__":
    logging.basicConfig(filename='app.log', filemode='w', format='[ %(levelname)s | %(asctime)s ]: - %(message)s',
                        level=0)
    bd = sqlite3.connect("basedata_test.db")
    BDHelper.init_from_file("test_init_bd_helper.txt")
    print(BDHelper.get_items(bd, "works"))
    # print(BDHelper.get_value(bd, "users", None, {"username": 'Veji', "password": '12345678'}, one_element=True))
    # print(BDHelper.get_page_count(bd, "chapters", {"id_work": 'Mandy'}, -1))
    # print(BDHelper.get_value(bd, "users", ["user_name"], {"user_id": 2}, one_element=True))
    # print(BDHelper.del_element(bd, "users", {"user_id": 2}))
    # print(BDHelper.get_value(bd, "users", ["user_name"], {"user_id": 2}, one_element=True))
    # BDHelper.add_element(bd, "users", {"user_name": "Veji", "role": 2}, ["user_name", "user_id"])
    # print(BDHelper.update_element(bd, "comments", {"manga_rating": 5}, {"user_id": 2}))
    # print(BDHelper.get_value(bd, "comments", None, {"user_id": 2}))
