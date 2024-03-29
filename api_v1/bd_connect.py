import os
import sqlite3
from werkzeug.datastructures import FileStorage
import api_v1.exception
import api_v1.genre_template


class BDConnect:
    BD_NAME = "bd_comics"

    @staticmethod
    def sql_command(bd_connection: sqlite3.Connection, command: str):
        """ Return list row from db """
        cursor = bd_connection.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        cursor.close()
        return data

    @staticmethod
    def sql_command_one(bd_connection: sqlite3.Connection, command: str):
        """ Return one row from db, only for primary key """
        cursor = bd_connection.cursor()
        cursor.execute(command)
        data = cursor.fetchone()
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
            },
                                      comments_list))
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
            },
                                      comments_list))
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
    def is_user_authorization(bd_connection: sqlite3.Connection, login: str, password: str) -> bool:
        return BDConnect.get_user_login(bd_connection, login, password)["login_is_successful"]

    @staticmethod
    def get_user_permission_level(bd_connection: sqlite3.Connection, login: str, password: str):
        if not BDConnect.is_user_authorization(bd_connection, login, password):
            return -1
        sql_command = f"SELECT role FROM users WHERE user_name = '{login}' and user_password = '{password}';"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data:
            return -1
        return data[0][-1]

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
    def get_catalog_manga(bd_connection: sqlite3.Connection, offset: int, limit: int, template: str = None):
        heads = tuple(
            map(lambda x: x[1], BDConnect.sql_command(bd_connection, f"PRAGMA table_info('manga');")))
        if template is None:
            sql_command = f"SELECT * FROM manga LIMIT {limit} OFFSET {offset}"
        else:
            sql_command = f"SELECT * FROM manga WHERE manga_types LIKE '{template}' LIMIT {limit} OFFSET {offset};"
        result = {
            "header_list": list(heads),
            "data_list": []
        }
        for i in BDConnect.sql_command(bd_connection, sql_command):
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

    @staticmethod
    def get_works_catalog(
            bd_connection: sqlite3.Connection,
            limit: int = -1, offset: int = 0, template: str = None, search_name: str = None
    ) -> dict:
        """ Return list of works """
        if template is not None and search_name is not None:
            sql_command = f"SELECT * FROM manga " \
                          f"WHERE manga_types LIKE '{template}' " \
                          f"and rus_manga_name LIKE '%' || lower('{search_name}') || '%' " \
                          f"LIMIT {limit} OFFSET {offset};"
            condition = f"WHERE manga_types LIKE '{template}' " \
                        f"and rus_manga_name LIKE '%' || lower('{search_name}') || '%'"
        elif template is not None and search_name is None:
            sql_command = f"SELECT * FROM manga WHERE manga_types LIKE '{template}' LIMIT {limit} OFFSET {offset};"
            condition = f"WHERE manga_types LIKE '{template}'"
        elif template is None and search_name is not None:
            sql_command = \
                f"SELECT * FROM manga " \
                f"WHERE lower(rus_manga_name) LIKE '%' || lower('{search_name}') || '%' LIMIT {limit} OFFSET {offset};"
            condition = f"WHERE lower(rus_manga_name) LIKE '%' || lower('{search_name}') || '%'"
        else:
            sql_command = f"SELECT * FROM manga LIMIT {limit} OFFSET {offset};"
            condition = ""
        data = {
            "catalog": [],
            "pages_count": BDConnect.get_works_comment_pages_count(bd_connection, "manga", condition, limit)
        }
        for work in BDConnect.sql_command(bd_connection, sql_command):
            data["catalog"].append({
                "id": work[0],
                "ru_name": work[1],
                "desc": work[2],
                "pre_img": work[3],
                "genre": work[4]
            })
        return data

    @staticmethod
    def get_catalog_search(bd_connection: sqlite3.Connection, limt: int, offs: int, temp: str):
        """ Return list of works """
        sql_command = \
            f"SELECT * FROM manga " \
            f"WHERE lower(rus_manga_name) LIKE '%' || lower('{temp}') || '%' LIMIT {limt} OFFSET {offs};"
        data = {
            "catalog": []
        }
        for work in BDConnect.sql_command(bd_connection, sql_command):
            data["catalog"].append({
                "id": work[0],
                "ru_name": work[1],
                "desc": work[2],
                "pre_img": work[3],
                "genre": work[4]
            })
        return data

    @staticmethod
    def is_work_id_exists(bd_connection: sqlite3.Connection, work_id: str):
        """ Return True if id is exists """
        sql_command = f"SELECT manga_name FROM manga WHERE manga_name == '{work_id}';"
        if BDConnect.sql_command(bd_connection, sql_command):
            return True
        return False

    @staticmethod
    def work_chapter_exists(bd_connection: sqlite3.Connection, work_id: str, chapter_num: int):
        sql_command = f"SELECT * FROM chapters WHERE manga_name = '{work_id}' and chapter_number = '{chapter_num}';"
        return BDConnect.sql_command(bd_connection, sql_command)

    @staticmethod
    def work_chapter_page_exists(bd_connection: sqlite3.Connection, work_id: str, c_num: int, p_num: int):
        sql_command = f"SELECT * FROM pages " \
                      f"WHERE manga_name = '{work_id}' and chapter_number = '{c_num}' and page_number = '{p_num}';"
        return BDConnect.sql_command(bd_connection, sql_command)

    @staticmethod
    def _add_file(bd_connection: sqlite3.Connection, file_path: str, file_name: str,
                  file: FileStorage, check_exists_path: bool = True):
        """ Return id file if file added else -1 """
        file_path = "manga/" + file_path + "/"
        if os.path.exists(file_path + file_name) and check_exists_path:
            return False
        if not os.path.exists(file_path) and check_exists_path:
            os.mkdir(file_path)
        sql_command = f"INSERT INTO files (image_path, image_name, image_format) " \
                      f"VALUES ('{file_path}', '{file_name}', '{file_name.split('.')[-1]}')" \
                      f"RETURNING image_id;"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data:
            return -1
        bd_connection.commit()
        file.save(file_path + file_name)
        file.close()
        return data[0][-1]

    @staticmethod
    def add_work(
            bd_connection: sqlite3.Connection, work_id: str, ru_name: str, desc: str, temp: str, file: FileStorage):
        if BDConnect.is_work_id_exists(bd_connection, work_id):
            return False
        if not api_v1.genre_template.Genre.is_english_alphabet(work_id):
            return False
        if file.filename.split(".")[-1] != "jpg":
            return False
        file_name = work_id + "_preview_image.jpg"
        file_id = BDConnect._add_file(bd_connection, work_id, file_name, file)
        sql_command = f"INSERT INTO manga " \
                      f"(manga_name, rus_manga_name, manga_description, manga_title_image, manga_types)" \
                      f"VALUES ('{work_id}', '{ru_name}', '{desc}', {file_id}, '{temp}') " \
                      f"RETURNING manga_name;"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not data:
            return False
        bd_connection.commit()
        return True

    @staticmethod
    def add_work_chapter(
            bd_connection: sqlite3.Connection,
            work_id: str,
            chapter_name: str,
            chapter_num: int,
            files: list[FileStorage]
    ):
        files_path = "/".join([work_id, f"chapter_{chapter_num}"])
        files_page_id = []
        if not BDConnect.is_work_id_exists(bd_connection, work_id):
            return False
        if os.path.exists("manga/" + files_path):
            return False
        if BDConnect.work_chapter_exists(bd_connection, work_id, chapter_num):
            return False
        os.mkdir("manga/" + files_path)
        for i in range(len(files)):
            added_file = BDConnect._add_file(bd_connection, files_path, f"img_{i + 1}.jpg", files[i], False)
            if not added_file:
                return False
            files_page_id.append(added_file)

        for i in range(len(files_page_id)):
            sql_command = f"INSERT INTO pages (manga_name, chapter_number, page_number, pages_image) " \
                          f"VALUES ('{work_id}', '{chapter_num}', '{i + 1}', '{files_page_id[i]}');"
            BDConnect.sql_command(bd_connection, sql_command)
        sql_command = f"INSERT INTO chapters (manga_name, chapter_name, chapter_number, chapter_len) " \
            f"VALUES ('{work_id}', '{chapter_name}', '{chapter_num}', {len(files_page_id)});"
        BDConnect.sql_command(bd_connection, sql_command)
        bd_connection.commit()
        return True

    @staticmethod
    def get_work(bd_connection: sqlite3.Connection, work_id: str) -> dict | None:
        sql_command = f"SELECT * FROM manga WHERE manga_name = '{work_id}';"
        data = BDConnect.sql_command_one(bd_connection, sql_command)
        if data:
            data = {
                "work_id": data[0],
                "ru_name": data[1],
                "desc": data[2],
                "pre_img": data[3],
                "genre": data[4]
            }
            return data

    @staticmethod
    def get_work_chapters(bd_connection: sqlite3.Connection, work_id: str) -> list | None:
        sql_command = f"SELECT * FROM chapters WHERE manga_name = '{work_id}';"
        data = BDConnect.sql_command(bd_connection, sql_command)
        if not BDConnect.get_work(bd_connection, work_id):
            return None
        if data:
            for i in range(len(data)):
                buff = {
                    "chapter_name": data[i][1],
                    "chapter_number": data[i][2],
                    "number_of_pages": data[i][3]
                }
                data[i] = buff
            return sorted(data, key=lambda x: x["chapter_number"])
        return []

    @staticmethod
    def get_user_info(bd_connection: sqlite3.Connection, username: str, password: str) -> dict | None:
        if not BDConnect.is_user_authorization(bd_connection, username, password):
            return None
        sql_command = f"SELECT * FROM users WHERE user_name = '{username}' and user_password = '{password}';"
        data = BDConnect.sql_command_one(bd_connection, sql_command)
        if data:
            return {
                "ID": data[0],
                "USERNAME": data[1],
                "ROLE": data[3]
            }
        return None

    @staticmethod
    def is_user_exists(bd_connection: sqlite3.Connection, user_id: int):
        sql_command = f"SELECT * FROM users WHERE user_id = '{user_id}';"
        data = BDConnect.sql_command_one(bd_connection, sql_command)
        if data:
            return {
                "ID": data[0],
                "USERNAME": data[1],
                "ROLE": data[3]
            }
        return None

    @staticmethod
    def get_user_likes_catalog(
            bd_connection: sqlite3.Connection, user_id: int, limit: int = -1, offset: int = 0) -> dict | None:
        if not BDConnect.is_user_exists(bd_connection, user_id):
            return None
        sql_command = f"SELECT * FROM user_likes_catalog WHERE user_id = '{user_id}' LIMIT {limit} OFFSET {offset};"
        count = BDConnect.get_works_comment_pages_count(
            bd_connection, "user_likes_catalog", f"WHERE user_id = '{user_id}'", limit)
        data = BDConnect.sql_command(bd_connection, sql_command)
        for i in range(len(data)):
            data[i] = BDConnect.get_work(bd_connection, data[i][1])
        return {"pages_count": count, "likes_list": data}

    @staticmethod
    def is_user_like_work(bd_connection: sqlite3.Connection, user_id: int, work_id: str):
        if not BDConnect.is_user_exists(bd_connection, user_id):
            return None
        if not BDConnect.is_work_id_exists(bd_connection, work_id):
            return None
        sql_command = f"SELECT * FROM user_likes_catalog WHERE  user_id = '{user_id}' and manga_name = '{work_id}';"
        data = BDConnect.sql_command_one(bd_connection, sql_command)
        return data is not None

    @staticmethod
    def set_user_like_work(bd_connection: sqlite3.Connection, user_id: int, work_id: str):
        res = False
        if not BDConnect.is_user_exists(bd_connection, user_id):
            return None
        if not BDConnect.is_work_id_exists(bd_connection, work_id):
            return None
        if BDConnect.is_user_like_work(bd_connection, user_id, work_id):
            sql_command = f"DELETE FROM user_likes_catalog WHERE user_id = '{user_id}' and manga_name = '{work_id}';"
        else:
            sql_command = f"INSERT INTO user_likes_catalog (user_id, manga_name) VALUES ({user_id}, '{work_id}');"
            res = True
        BDConnect.sql_command(bd_connection, sql_command)
        bd_connection.commit()
        return res

    @staticmethod
    def get_user_comment_list(
            bd_connection: sqlite3.Connection, user_id: int, limit: int = -1, offset: int = 0) -> dict | None:
        if not BDConnect.is_user_exists(bd_connection, user_id):
            return None
        sql_command = f"SELECT * FROM comments WHERE user_id = '{user_id}' LIMIT {limit} OFFSET {offset};"
        data = BDConnect.sql_command(bd_connection, sql_command)
        for i in range(len(data)):
            work = BDConnect.get_work(bd_connection, data[i][1])
            if work is None:
                work = {"ru_name": "None", "pre_img": "None"}
            buff = {
                "work_id": data[i][1],
                "grade": data[i][2],
                "comment": data[i][3],
                "ru_name": work["ru_name"],
                "pre_img": work["pre_img"]
            }
            data[i] = buff
        return {
            "user_comments_list": data,
            "user_id": user_id,
            "pages_count": BDConnect.get_works_comment_pages_count(
                bd_connection, "comments", f"WHERE user_id = '{user_id}'", limit)
        }

    @staticmethod
    def get_user_comment(bd_connection: sqlite3.Connection, user_id: int, work_id: str):
        """ Return none if user is not authorization, {} - if No comment """
        if not BDConnect.is_user_exists(bd_connection, user_id):
            raise api_v1.exception.NotExists(f"User {user_id} is not exists")
        if not BDConnect.is_work_id_exists(bd_connection, work_id):
            raise api_v1.exception.NotExists(f"Work {work_id} is not exists")
        sql_command = f"SELECT * FROM comments WHERE manga_name = '{work_id}' and user_id = '{user_id}';"
        data = BDConnect.sql_command_one(bd_connection, sql_command)
        if data:
            return {
                "comment_exists": True,
                "username": BDConnect.get_username(bd_connection, data[0]),
                "work_id": data[1],
                "rating": data[2],
                "comment": data[3]
            }
        return {"comment_exists": False}

    @staticmethod
    def get_username(bd_connection: sqlite3.Connection, user_id: str):
        sql_command = f"SELECT user_name FROM users WHERE user_id = '{user_id}'"
        data = BDConnect.sql_command_one(bd_connection, sql_command)
        if data:
            return data[0]

    @staticmethod
    def get_works_comment_pages_count(
            bd_connection: sqlite3.Connection, table_name: str, condition: str = "", limit: int = -1):
        sql_command = f"SELECT COUNT(*) FROM {table_name} {condition};"
        data = BDConnect.sql_command_one(bd_connection, sql_command)
        if data:
            data = data[0]
        if data is None or limit is None:
            return 1
        if data == 0 or limit <= 0:
            return 1
        if data % limit == 0:
            return data // limit
        return int(data / limit) + 1

    @staticmethod
    def get_work_comments_list(
            bd_connection: sqlite3.Connection, work_id: str, limit: int, offset: int, but_user: int = None):
        if not BDConnect.is_work_id_exists(bd_connection, work_id):
            return None
        if but_user is None:
            sql_command = f"SELECT * FROM comments WHERE manga_name = '{work_id}' LIMIT {limit} OFFSET {offset};"
            condition = f" WHERE manga_name = '{work_id}' LIMIT {limit} OFFSET {offset}"
        else:
            sql_command = f"SELECT * FROM comments " \
                          f"WHERE manga_name = '{work_id}' " \
                          f"and user_id NOT LIKE {but_user} LIMIT {limit} OFFSET {offset};"
            condition = f" WHERE manga_name = '{work_id}' and user_id NOT LIKE {but_user}"
        data = BDConnect.sql_command(bd_connection, sql_command)
        for i in range(len(data)):
            buff = {
                "user_id": data[i][0],
                "username": BDConnect.get_username(bd_connection, data[i][0]),
                "rating": data[i][2],
                "comment": data[i][3]
            }
            if buff["username"] is None:
                buff["username"] = "Not found user"
            data[i] = buff
        return {
            "work_id": work_id,
            "comments-list": data,
            "pages_count": BDConnect.get_works_comment_pages_count(bd_connection, "comments", condition, limit)
        }

    @staticmethod
    def del_works_comment(bd_connection: sqlite3.Connection, user_id: int, work_id: str):
        sql_command = f"DELETE FROM comments WHERE user_id = {user_id} and manga_name = '{work_id}';"
        BDConnect.sql_command_one(bd_connection, sql_command)
        bd_connection.commit()

    @staticmethod
    def append_works_comment(
            bd_connection: sqlite3.Connection, user_id: int, work_id: str, rating: int, comment: str):
        usr_comm = BDConnect.get_user_comment(bd_connection, user_id, work_id)
        if usr_comm["comment_exists"]:
            raise api_v1.exception.AppendCollision(f"User {user_id} write comment to work: {work_id}")
        sql_command = f"INSERT INTO comments (user_id, manga_name, manga_rating, comment) " \
                      f"VALUES ('{user_id}', '{work_id}', '{rating}', '{comment}');"
        BDConnect.sql_command_one(bd_connection, sql_command)
        bd_connection.commit()

    @staticmethod
    def update_works_comment(bd_connection: sqlite3.Connection, user_id: int, work_id: str, rating: int, comment: str):
        usr_comm = BDConnect.get_user_comment(bd_connection, user_id, work_id)
        if not usr_comm["comment_exists"]:
            raise api_v1.exception.NotExists("Comment not created! Use POST method")
        sql_command = f"UPDATE comments " \
                      f"SET comment = '{comment}', manga_rating = '{rating}' " \
                      f"WHERE user_id = '{user_id}' and manga_name = '{work_id}';"
        BDConnect.sql_command_one(bd_connection, sql_command)
        bd_connection.commit()
        return True

    @staticmethod
    def get_awg_rating_work(bd_connection: sqlite3.Connection, work_id: str):
        if not BDConnect.is_work_id_exists(bd_connection, work_id):
            raise api_v1.exception.NotExists(f"Work {work_id} is not exists")
        sql_command = f"SELECT AVG(manga_rating) FROM comments WHERE manga_name = '{work_id}';"
        data = BDConnect.sql_command_one(bd_connection, sql_command)[0]
        return data if data is not None else 0

    @staticmethod
    def del_work(bd_connection: sqlite3.Connection, work_id: str):
        """ Exception delete files from all bd """
        sql_command = f"DELETE FROM manga WHERE manga_name = '{work_id}' RETURNING manga_title_image;"
        title_image = BDConnect.sql_command_one(bd_connection, sql_command)

        sql_command = f"DELETE FROM pages WHERE manga_name = '{work_id}' RETURNING pages_image;"
        files_id = list(map(lambda x: x[0], BDConnect.sql_command(bd_connection, sql_command)))
        path = []
        for i in files_id:
            sql_command_file = f"DELETE FROM files WHERE image_id = '{i}' RETURNING image_path, image_name;"
            if i == title_image:
                continue
            file = BDConnect.sql_command_one(bd_connection, sql_command_file)
            if os.path.exists("".join(file)):
                os.remove("".join(file))
            path.append(file[0])
        sql_command = f"DELETE FROM chapters WHERE manga_name = '{work_id}';"
        BDConnect.sql_command(bd_connection, sql_command)
        sql_command = f"DELETE FROM comments WHERE manga_name = '{work_id}';"
        BDConnect.sql_command(bd_connection, sql_command)
        sql_command = f"DELETE FROM pages WHERE manga_name = '{work_id}';"
        BDConnect.sql_command(bd_connection, sql_command)
        sql_command = f"DELETE FROM user_likes_catalog WHERE manga_name = '{work_id}';"
        BDConnect.sql_command(bd_connection, sql_command)
        sql_command_file = f"DELETE FROM files WHERE image_id = '{title_image[0]}' RETURNING image_path, image_name;"
        file = BDConnect.sql_command_one(bd_connection, sql_command_file)
        if os.path.exists("".join(file)):
            os.remove("".join(file))
        for i in path:
            if os.path.exists(i):
                os.rmdir(i)
        if os.path.exists(file[0]):
            os.rmdir(file[0])
        bd_connection.commit()
        return True

    @staticmethod
    def user_reg(bd_connection: sqlite3.Connection, username: str, password: str):
        sql_command = f"INSERT INTO users (user_name, user_password) " \
                      f"VALUES ('{username}', '{password}') RETURNING user_id, user_name, role;"
        data = BDConnect.sql_command_one(bd_connection, sql_command)
        bd_connection.commit()
        return {
            "ID": data[0],
            "USERNAME": data[1],
            "USER_ROLE": data[2]
        }


if __name__ == "__main__":
    bd = sqlite3.connect(BDConnect.BD_NAME)
    print(BDConnect.user_reg(bd, "bd_conn_2", "haha"))
    # print(BDConnect.add_work_chapter(bd, "Dragon_lady", "Кофе", 1, 0, []))
    # pprint.pprint(BDConnect._add_file(bd, "resists", "test.jpg", None))
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
