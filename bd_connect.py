import os
import pprint
import sqlite3


class BDConnect:
    BD_NAME = "bd_comics"

    @staticmethod
    def sql_command(bd_connection: sqlite3.Connection, command: str):
        cursor = bd_connection.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        cursor.close()
        return data

    @staticmethod
    def add_manga_in_like_manga_user(
            bd_connection: sqlite3.Connection, user_name: str, user_password: str, mid: str
    ) -> dict | None:
        data = BDConnect.get_like_manga_user(bd_connection, user_name, user_password)
        if not data["user_authorization"]:
            return {"user_authorization": False}
        sql_command = f"SELECT * FROM users WHERE user_name = '{user_name}';"
        user_id = BDConnect.sql_command(bd_connection, sql_command)
        if not user_id:
            return {"user_authorization": False}
        else:
            user_id = user_id[0][0]
        if mid in data["user_like_manga_list"]:
            sql_command = (f"DELETE FROM user_likes_catalog"
                           f" WHERE user_id = '{user_id}' AND manga_name = '{mid}';")
            BDConnect.sql_command(bd_connection, sql_command)
            bd_connection.commit()
            return {
                "user_authorization": True,
                "manga_id": mid,
                "manga_in_user_like_manga": False
            }
        if mid not in data["user_like_manga_list"]:
            manga_list = BDConnect.get_list_manga_name(bd_connection)
            if manga_list and mid in manga_list["list_manga_name"]:
                sql_command = (f"INSERT INTO user_likes_catalog(user_id, manga_name)"
                               f"VALUES('{user_id}', '{mid}')")
                BDConnect.sql_command(bd_connection, sql_command)
                bd_connection.commit()
                return {
                    "user_authorization": True,
                    "manga_id": mid,
                    "manga_in_user_like_manga": True
                }
        return {
            "user_authorization": True,
            "manga_id": mid,
            "manga_in_user_like_manga": False
        }

    @staticmethod
    def delete_user_comment(bd_connection: sqlite3.Connection, lgn: str, psw: str, mid: str) -> dict:
        is_user = BDConnect.get_user_login(bd_connection, lgn, psw)
        if not is_user or not is_user["login_is_successful"]:
            return {"user_authorization": False, "commit": False}
        sql_command = f"SELECT * FROM users WHERE user_name = '{lgn}';"
        user_id = BDConnect.sql_command(bd_connection, sql_command)
        if not user_id:
            return {"user_authorization": False, "commit": False}
        else:
            user_id = user_id[0][0]
        sql_command = f"DELETE FROM comments WHERE user_id = '{user_id}' AND manga_name = '{mid}'"
        data = BDConnect.get_comments_list(bd_connection, mid)
        for i in data["comments_list"]:
            if i["user_name"] == lgn and i["manga_name"] == mid:
                BDConnect.sql_command(bd_connection, sql_command)
                bd_connection.commit()
                return {"user_authorization": True, "commit": True}
        return {"user_authorization": True, "commit": False}

    @staticmethod
    def get_user_comments_list(bd_connection: sqlite3.Connection, lgn: str, psw: str):
        is_user = BDConnect.get_user_login(bd_connection, lgn, psw)
        if not is_user or not is_user["login_is_successful"]:
            return {"user_authorization": False, "commit": False}
        sql_command = f"SELECT * FROM users WHERE user_name = '{lgn}';"
        user_id = BDConnect.sql_command(bd_connection, sql_command)
        if not user_id:
            return {"user_authorization": False, "commit": False}
        else:
            user_id = user_id[0][0]
        sql_command = f"SELECT * FROM comments WHERE user_id = '{user_id}';"
        comments_list = BDConnect.sql_command(bd_connection, sql_command)
        comments_list = {
            "user_authorization": True,
            "comments_count": len(comments_list),
            "comments_list": list(map(lambda x: {
                "user_name": BDConnect.sql_command(
                    bd_connection, f"SELECT * FROM users WHERE user_id = '{x[0]}';")[0][1],
                "user_id": x[0],
                "manga_name": x[1],
                "manga_rating": x[2],
                "manga_comment": x[3]
            }
                                      , comments_list))
        }
        return comments_list

    @staticmethod
    def is_user_set_comment(bd_connection: sqlite3.Connection, user_name: str, mid: str) -> dict:
        data = BDConnect.get_comments_list(bd_connection, mid)
        for i in data["comments_list"]:
            if i["user_name"] == user_name:
                return {
                    "user_authorization": True,
                    "commit": True
                }
        return {
            "user_authorization": True,
            "commit": False
        }

    @staticmethod
    def get_comment(bd_connection: sqlite3.Connection, mid: str, user_name: str) -> dict | None:
        data = BDConnect.get_comments_list(bd_connection, mid)
        if data:
            for item in data["comments_list"]:
                if item["user_name"] == user_name:
                    return item
        return None

    @staticmethod
    def get_comments_list(bd_connection: sqlite3.Connection, mid: str) -> dict:
        """ Получение комментариев к манге """
        sql_command = f"SELECT * FROM comments WHERE manga_name = '{mid}'"
        comments_list = BDConnect.sql_command(bd_connection, sql_command)
        comments_list = {
            "comments_count": len(comments_list),
            "manga_name": mid,
            "comments_list": list(map(lambda x: {
                "user_name": BDConnect.sql_command(
                    bd_connection, f"SELECT * FROM users WHERE user_id = '{x[0]}';")[0][1],
                "user_id": x[0],
                "manga_name": x[1],
                "manga_rating": x[2],
                "manga_comment": x[3]
            }
                                      , comments_list))
        }
        return comments_list

    @staticmethod
    def add_comments(
            bd_connection: sqlite3.Connection,
            user_name: str, user_password: str,
            mid: str, comment: str, rating: int
    ):
        """ Добавление комментария """
        if not BDConnect.is_user(bd_connection, user_name):
            return {"user_authorization": False}
        if not BDConnect.get_user_login(bd_connection, user_name, user_password)["login_is_successful"]:
            return {"user_authorization": False}
        sql_command = f"SELECT * FROM users WHERE user_name = '{user_name}';"
        user_id = BDConnect.sql_command(bd_connection, sql_command)
        if not user_id:
            return {"user_authorization": False}
        else:
            user_id = user_id[0][0]
        sql_command = f"SELECT * FROM comments WHERE user_id = '{user_id}' AND manga_name = '{mid}';"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data:
            manga_list = BDConnect.get_list_manga_name(bd_connection)
            if manga_list and mid in manga_list["list_manga_name"]:
                comments_list = BDConnect.get_comments_list(bd_connection, mid)
                if user_id not in list(map(lambda x: x["user_id"], comments_list["comments_list"])):
                    sql_command = (f"INSERT INTO comments (user_id, manga_name, manga_rating, comment) "
                                   f"VALUES ('{user_id}', '{mid}', '{rating}', '{comment}');")
                    BDConnect.sql_command(bd_connection, sql_command)
                    bd_connection.commit()
                    return {"user_authorization": True, "commit": True}
        return {"user_authorization": True, "commit": False}

    @staticmethod
    def get_like_manga_user(bd_connection: sqlite3.Connection, user_name: str, user_password: str) -> dict | None:
        """ Получение списка понравившихся пользователю манг """
        if not BDConnect.is_user(bd_connection, user_name):
            return {"user_authorization": False}
        if not BDConnect.get_user_login(bd_connection, user_name, user_password)["login_is_successful"]:
            return {"user_authorization": False}
        sql_command = f"SELECT * FROM users WHERE user_name = '{user_name}';"
        user_id = BDConnect.sql_command(bd_connection, sql_command)
        if not user_id:
            return {"user_authorization": False}
        else:
            user_id = user_id[0][0]
        sql_command = f"SELECT * FROM user_likes_catalog WHERE user_id = '{user_id}';"
        user_like_maga_list = BDConnect.sql_command(bd_connection, sql_command)
        user_like_maga_list = list(map(lambda x: x[1], user_like_maga_list))
        return {
            "user_authorization": True,
            "user_like_manga_list": user_like_maga_list
        }

    @staticmethod
    def manga_in_likes_list(
            bd_connection: sqlite3.Connection,
            user_name: str,
            user_password: str,
            mid: str
    ) -> dict | None:
        """ Есть ли манга в списке понравившихся """
        data = BDConnect.get_like_manga_user(bd_connection, user_name, user_password)
        if not data or not data["user_authorization"] or type(mid) is not str:
            return {"user_authorization": False}
        return {
            "user_authorization": True,
            "manga_id": mid,
            "manga_in_user_manga_like_list": mid in data["user_like_manga_list"]
        }

    @staticmethod
    def is_user(bd_connection: sqlite3.Connection, user_name: str) -> bool:
        sql_command = f"SELECT * FROM users WHERE user_name = '{user_name}';"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if data:
            return True
        return False

    @staticmethod
    def user_registration(bd_connection: sqlite3.Connection, user_name: str, user_password: str) -> bool | None:
        sql_command = (f"INSERT INTO users (user_name, user_password) "
                       f"VALUES ('{user_name}', '{user_password}');")
        if not BDConnect.is_user(bd_connection, user_name):
            BDConnect.sql_command(bd_connection, sql_command)
            bd_connection.commit()
            return True
        return False

    @staticmethod
    def get_user_login(bd_connection: sqlite3.Connection, user_name: str, user_password: str) -> dict | None:
        sql_command = f"SELECT * FROM users WHERE user_name = '{user_name}';"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if data and data[0][1] == user_name and data[0][2] == user_password:
            return {"login_is_successful": True}
        return {"login_is_successful": False}

    @staticmethod
    def get_info_manga(bd_connection: sqlite3.Connection, manga_name: str) -> dict | None:
        sql_command = f"SELECT * FROM manga WHERE manga_name = '{manga_name}';"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data:
            return None
        return {
            "manga_name": data[0][0],
            "rus_manga_name": data[0][1],
            "manga_description": data[0][2],
            "manga_title_image": data[0][3]
        }

    @staticmethod
    def get_info_chapter(bd_connection: sqlite3.Connection, manga_name: str, chapter_number: int):
        sql_command = \
            f"SELECT chapter_name, chapter_len " \
            f"FROM chapters " \
            f"WHERE manga_name='{manga_name}' AND chapter_number = {chapter_number};"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data:
            return None
        return {
            "chapter_name": data[-1][0],
            "chapter_len": data[-1][1]
        }

    @staticmethod
    def get_list_manga_name(
            bd_connection: sqlite3.Connection, limit: int = -1, offset: int = 0, r: bool = False
    ) -> dict | None:
        sql_command = (f"SELECT manga_name FROM manga ORDER BY manga_name {'ASC' if r else 'DESC'}"
                       f" LIMIT {limit} OFFSET {offset} ;")
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data:
            return None
        return {
            "list_manga_name": list(map(lambda x: x[0], data))
        }

    @staticmethod
    def get_info_file(bd_connection: sqlite3.Connection, file_id: int) -> dict | None:
        sql_command = f"SELECT image_path, image_name, image_format FROM files WHERE image_id = {file_id};"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data:
            return None
        return {
            "image_path": data[0][0],
            "image_name": data[0][1],
            "image_format": data[0][2]
        }

    @staticmethod
    def get_file(bd_connection: sqlite3.Connection, file_id: int):
        sql_command = f"SELECT image_path, image_name, image_format FROM files WHERE image_id = {file_id};"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data or\
                not os.path.exists("".join([data[0][0], data[0][1]])) or\
                not os.path.isfile("".join([data[0][0], data[0][1]])):
            return None
        return open("".join([data[0][0], data[0][1]]), "rb")

    @staticmethod
    def get_list_manga_chapters(bd_connection: sqlite3.Connection, manga_name: str):
        sql_command = \
            f"SELECT chapter_number, chapter_name, chapter_len FROM chapters WHERE manga_name = '{manga_name}';"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data:
            return None
        return {
            "list_manga_chapters": list(map(lambda x: {
                "chapter_number": x[0], "chapter_name": x[1], "chapter_len": x[2]}, data))
        }

    @staticmethod
    def get_info_page(bd_connection: sqlite3.Connection, manga_name: str, chapter_number: int, page_number: int):
        sql_command = \
            f"SELECT pages_image " \
            f"FROM pages " \
            f"WHERE manga_name = '{manga_name}' " \
            f"AND chapter_number = {chapter_number} AND page_number = {page_number};"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data:
            return None
        return {"id_page_image": data[0][0]}

    @staticmethod
    def get_len_chapter(bd_connection: sqlite3.Connection, manga_name: str, chapter_number: int) -> int | None:
        sql_command = \
            f"SELECT page_number FROM pages WHERE  manga_name = '{manga_name}' AND chapter_number = {chapter_number};"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data:
            return None
        return len(data)

    @staticmethod
    def _add_chapter(
            manga_name: str,                # ID манги ( название на английском )
            chapter_name: str,              # Название главы
            chapter_num: int,               # Номер главы
            list_file_names: list[str],     # Список названий файлов страниц
            path_to_files: str              # Путь к файлам
    ):
        bd_connect = sqlite3.connect(BDConnect.BD_NAME)
        if not BDConnect.sql_command(bd_connect, f"SELECT * FROM manga WHERE manga_name = '{manga_name}';"):
            raise "manga has not in manga table"
        if BDConnect.get_info_chapter(bd_connect, manga_name, chapter_num):
            raise f"Chapter {chapter_num}|{chapter_name} is exist in {manga_name}"
        for _file_name in list_file_names:
            if not os.path.exists(path_to_files + _file_name) or not os.path.isfile(path_to_files + _file_name):
                raise f"File: {_file_name} - is incorrect !!! "
            if _file_name.split(".")[-1] != "jpg":
                raise f"File {_file_name} - incorrect format"
        sql_command = \
            f"INSERT INTO chapters (manga_name, chapter_name, chapter_number, chapter_len) " \
            f"VALUES ('{manga_name}', '{chapter_name}', {chapter_num}, {len(list_file_names)});"
        BDConnect.sql_command(bd_connect, sql_command)
        for _file_name in range(len(list_file_names)):
            sql_command = \
                f"INSERT INTO files (image_path, image_name, image_format) " \
                f"VALUES ('{path_to_files}', '{list_file_names[_file_name]}', 'jpg');"
            BDConnect.sql_command(bd_connect, sql_command)
            sql_command = "SELECT image_id FROM files ORDER BY image_id DESC LIMIT 1;"
            last_id = int(BDConnect.sql_command(bd_connect, sql_command)[0][0])
            sql_command = \
                f"INSERT INTO pages (manga_name, chapter_number, page_number, pages_image) " \
                f"VALUES ('{manga_name}', {chapter_num}, {_file_name+1}, {last_id});"
            BDConnect.sql_command(bd_connect, sql_command)

        bd_connect.commit()

    @staticmethod
    def get_bd_page(bd_connection: sqlite3.Connection, table_name: str, offset: int, limit: int):
        heads = tuple(
            map(lambda x: x[1], BDConnect.sql_command(bd_connection, f"PRAGMA table_info('{table_name}');")))
        sql_command = f"SELECT * FROM {table_name} LIMIT {limit} OFFSET {offset}"
        data = BDConnect.sql_command(bd_connection, sql_command)
        # print(heads)
        # print(data)
        result = {
            "header_list": list(heads),
            "data_list": []
        }
        for i in data:
            result["data_list"].append(
                {heads[index]: i[index] for index in range(len(heads))}
            )
        return result

    @staticmethod
    def api_get_user_info(bd_connection: sqlite3.Connection, user_name: str):
        sql_command = f"SELECT * FROM users WHERE user_name = '{user_name}'"
        data = BDConnect.sql_command(bd_connection, sql_command)
        result = {}
        if data:
            result["result"] = True
            result["user_id"] = data[0][0]
            result["user_name"] = data[0][1]
            result["user_password"] = data[0][2]
            result["role"] = data[0][3]
        else:
            result["result"] = False
        return result

    @staticmethod
    def api_get_manga_comments(
            bd_connection: sqlite3.Connection,
            manga_name: str, limit: int = -1, offset: int = 0):
        sql_command = f"SELECT * FROM comments WHERE manga_name = '{manga_name}' LIMIT {limit} OFFSET {offset}"
        data = BDConnect.sql_command(bd_connection, sql_command)
        result = {"result": False}
        if data:
            result["comments"] = list(map(lambda comment: {
                "user_name": "tets_user",
                "user_id": comment[0],
                "manga_name": comment[1],
                "manga_rating": comment[2],
                "comment": comment[3]
            }, data))
            result["result"] = True
        return result

    @staticmethod
    def get_user_read_catalog_list(
            bd_connection: sqlite3.Connection, user_name: str, user_password: str,
            limit: int = -1, offset: int = 0) -> dict:
        """ Получение списка прочитанных пользователем манг """
        result = {"result": False}
        if not BDConnect.is_user(bd_connection, user_name):
            return result
        if not BDConnect.get_user_login(bd_connection, user_name, user_password)["login_is_successful"]:
            return result
        sql_command = f"SELECT * FROM users WHERE user_name = '{user_name}';"
        user_id = BDConnect.sql_command(bd_connection, sql_command)
        if not user_id:
            return result
        else:
            user_id = user_id[0][0]
        sql_command = f"SELECT * FROM user_likes_catalog WHERE user_id = '{user_id}' LIMIT {limit} OFFSET {offset};"
        user_read_maga_list = BDConnect.sql_command(bd_connection, sql_command)
        user_read_maga_list = list(map(lambda x: x[1], user_read_maga_list))
        result["read_manga_list"] = []
        for item in user_read_maga_list:
            item_data = BDConnect.get_info_manga(bd_connection, item)
            if not item_data:
                return {"result": False}
            result["read_manga_list"].append(item_data)
        result["result"] = True
        result["size"] = len(user_read_maga_list)
        return result

    @staticmethod
    def get_user_comments(bd_connection: sqlite3.Connection, lgn: str, psw: str, limit: int = -1, offset: int = 0):
        is_user = BDConnect.get_user_login(bd_connection, lgn, psw)
        result = {"result": False}
        if not is_user or not is_user["login_is_successful"]:
            return result
        sql_command = f"SELECT * FROM users WHERE user_name = '{lgn}';"
        user_id = BDConnect.sql_command(bd_connection, sql_command)
        if not user_id:
            return result
        else:
            user_id = user_id[0][0]
        sql_command = f"SELECT * FROM comments WHERE user_id = '{user_id}' LIMIT {limit} OFFSET {offset};"
        comments_list = BDConnect.sql_command(bd_connection, sql_command)
        if comments_list:
            result["result"] = True
            result["comments"] = []
            for item in comments_list:
                manga_name = BDConnect.get_info_manga(bd_connection, item[1])
                result["comments"].append(
                    {
                        "rus_manga_name": manga_name["rus_manga_name"],
                        "manga_name": item[1],
                        "manga_rating": item[2],
                        "comment": item[3]
                    }
                )
        return result


if __name__ == "__main__":
    bd = sqlite3.connect(BDConnect.BD_NAME)
    pprint.pprint(BDConnect.get_user_comments(bd, "Veji", "1k75d45t80"))
    # pprint.pprint(BDConnect.get_user_read_catalog_list(bd, "Veji", "1k75d45t80", 1, 1))
    # pprint.pprint(BDConnect.api_get_manga_comments(bd, "I_want_my_hat_back", 1, 2))
    # print(BDConnect.get_bd_page(bd, "manga", 0, 10))
    # print(BDConnect.add_comments(bd, "Shelby", "12345678", "Mandy", "Nice Manga", 7))
    # print(BDConnect.get_comments(bd, "Mandy"))

    # print(BDConnect.add_manga_in_like_manga_user(bd, "Shelby", "12345678", "Mandy"))
    # print(BDConnect.get_user_comments_list(bd, "Shelby", "12345678"))
    # print(BDConnect.manga_in_likes_list(bd, "Shelby", "12345678", "Mandy"))
    # print(BDConnect.get_user_login(bd, "adin", "admin"))
    # print(BDConnect.user_registration(bd, "Nickolay", "1234"))

    # print(BDConnect.sql_command(bd, "SELECT image_id FROM files ORDER BY image_id DESC LIMIT 1;")[0][0])
    # print(BDConnect.get_list_manga_name(bd, -1, 0))
    # print(BDConnect.get_manga_info(bd, "Mandy"))
    # print(BDConnect.get_manga_name_list(bd))
    # print(BDConnect.get_file_info(bd, 1))
    # print(BDConnect.get_file(bd, 13))
    # print(BDConnect.get_list_manga_chapters(bd, "Mandy"))
    # print(BDConnect.get_info_page(bd, 'Mandy', 1, 1))
    # print(BDConnect.get_len_chapter(bd, "Mandy", 1))
    # BDConnect._add_chapter(
    #     "I_want_my_hat_back",
    #     " ",
    #     1,
    #     [f"img_{i}.jpg" for i in range(1, 14)],
    #     "manga/I_want_my_hat_back/chapter_1/"