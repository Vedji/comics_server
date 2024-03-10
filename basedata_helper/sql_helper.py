import sqlite3


class SQLiteHelperBD:
    @staticmethod
    def execute_all(bd_connection: sqlite3.Connection, command: str):
        """ Return list row from db """
        cursor = bd_connection.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        cursor.close()
        return data

    @staticmethod
    def execute_one(bd_connection: sqlite3.Connection, command: str):
        """ Return list row from db """
        cursor = bd_connection.cursor()
        cursor.execute(command)
        data = cursor.fetchone()
        cursor.close()
        return data

    @staticmethod
    def execute_commit_one(bd_connection: sqlite3.Connection, command: str):
        """ Return list row from db """
        cursor = bd_connection.cursor()
        cursor.execute(command)
        data = cursor.fetchone()
        bd_connection.commit()
        cursor.close()
        return data

    @staticmethod
    def execute_commit_all(bd_connection: sqlite3.Connection, command: str):
        """ Return list row from db """
        cursor = bd_connection.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        bd_connection.commit()
        cursor.close()
        return data


if __name__ == "__main__":
    pass