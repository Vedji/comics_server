import sqlite3
import time

import requests
from bs4 import BeautifulSoup

class BDAdmin:
    BD_NAME = "bd_comics"

    @staticmethod
    def sql_command(bd_connection: sqlite3.Connection, command: str):
        cursor = bd_connection.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        cursor.close()
        return data

    @staticmethod
    def _add_file(
            bd_connection: sqlite3.Connection,
            path_to_file: str, file_name: str, file_type: str = "jpg"
    ) -> None:
        sql_command = (f"INSERT INTO files (image_path, image_name, image_format)"
                       f" VALUES ('{path_to_file}', '{file_name}', '{file_type}')")
        BDAdmin.sql_command(bd_connection, sql_command)
        bd_connection.commit()

    @staticmethod
    def add_files(
            bd_connection: sqlite3.Connection,
            path_to_file: str, end_file_number: int, file_name_patter: str = "img_{}.jpg", file_type: str = "jpg"):
        for index in range(1, end_file_number + 1):
            BDAdmin._add_file(bd_connection, path_to_file, file_name_patter.format(index), file_type)
        bd_connection.commit()

    @staticmethod
    def _add_page(
            bd_connection: sqlite3.Connection,
            manga_name: str, chapter_number: int, page_number: int, pages_image: int
    ):
        sql_command = (f"INSERT INTO pages (manga_name, chapter_number, page_number, pages_image)"
                       f" VALUES ('{manga_name}', '{chapter_number}', '{page_number}', '{pages_image}')")
        BDAdmin.sql_command(bd_connection, sql_command)
        bd_connection.commit()

    @staticmethod
    def add_pages(bd_connection: sqlite3.Connection,
                  manga_name: str, chapter_number: int, page_number_end: int, pages_image_id_start: int):
        for index in range(1, page_number_end + 1):
            BDAdmin._add_page(bd_connection, manga_name, chapter_number, index, pages_image_id_start)
            pages_image_id_start += 1

    @staticmethod
    def _add_chapter(bd_connection: sqlite3.Connection,
                     manga_name: str, chapter_name: str, chapter_number: int, chapter_len: int,
                     pages_image_id_start: int):

        BDAdmin.add_pages(bd_connection, manga_name, chapter_number, chapter_len, pages_image_id_start)
        sql_command = (f"INSERT INTO chapters (manga_name, chapter_name, chapter_number, chapter_len) "
                       f"VALUES ('{manga_name}', '{chapter_name}', '{chapter_number}', '{chapter_len}')")
        BDAdmin.sql_command(bd_connection, sql_command)

    @staticmethod
    def get_last_image(bd_connection: sqlite3.Connection, image_path: str) -> int:
        sql_command = f"SELECT * FROM files WHERE image_path = '{image_path}'"
        data = BDAdmin.sql_command(bd_connection, sql_command)
        data = list(min(data, key=lambda x: x[0]))
        return data[0]

    @staticmethod
    def interface_add_chapter(bd_connection: sqlite3.Connection):
        manga_id = input("Индификатор манги: ")
        path_to_file = input("Путь к файлам: ")
        chapter_name = input("Название главы манги: ")
        chapter_number = int(input("Номер главы манги: "))
        chapter_len = int(input("Количество страниц в главе: "))
        print("Проверка")
        print("\tpath_to_file: '{}'".format(path_to_file))
        print("\tchapter_len: '{}'".format(chapter_len))
        print("\tmanga_id: '{}'".format(manga_id))
        print("\tchapter_name: '{}'".format(chapter_name))
        print("\tchapter_number: '{}'".format(chapter_number))
        print("\n")
        if input("y/n") == 'n':
            return
        print("\n")
        BDAdmin.add_files(bd_connection, path_to_file, chapter_len)
        start_file_id = int(BDAdmin.get_last_image(bd_connection, path_to_file))
        BDAdmin._add_chapter(bd_connection, manga_id, chapter_name, chapter_number, chapter_len, start_file_id)
        bd_connection.commit()


if __name__ == "__main__":
    bd = sqlite3.connect(BDAdmin.BD_NAME)
    BDAdmin.interface_add_chapter(bd)
    # BDAdmin.add_pages(bd, "The_Amazing_Spider_Man", 2, 23, 175)
    # BDAdmin.add_files(bd, "manga/The_Amazing_Spider_Man/chapter_2/", 23)
    # BDAdmin.add_file(bd "test/", "file_name")
    # BDAdmin.add_page(bd, "The_Amazing_Spider_Man", 1, 45, 174)

    # manga/Iron_Man/chapter_1/
    # Iron_Man

    # path_to_file: 'manga/Iron_Man/chapter_2/'
    # chapter_len: '23'
    # manga_id: 'Iron_Man'
    # chapter_name: 'Том 1 Глава 2 - Вера: асть 2. Ставка для джентельмена'
    # chapter_number: '2'
