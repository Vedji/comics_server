import pprint
import sqlite3
import re
import datetime
import basedata_helper.bd_unit
import basedata_helper.bd_helper


class BDWork(basedata_helper.bd_unit.BDUnit):
    TABLE_NAME = "works"
    PRIMARY_KEYS = ["id_work"]
    KEYS = [
        "id_work",
        "id_user",
        "added_datatime",
        "id_preview_image",
        "fts",
        "rus_name",
        "eng_name",
        "description",
        "genres"
    ]

    @classmethod
    def append_item(cls, bd_connection: sqlite3.Connection, added_values: dict) -> dict | None:
        if "added_datatime" not in added_values:
            added_values = {**added_values, "added_datatime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        if "fts" not in added_values:
            added_values = {
                **added_values,
                "fts": added_values["rus_name"].lower() + " " + added_values["eng_name"].lower()
            }
        return super().append_item(bd_connection, added_values)

    @classmethod
    def ft_search_work(cls, bd_connection, fts: str, limit: int = -1, offset: int = 0):
        delimiters = "-_.,?!'\":;)("
        fts = " ".join(re.split(f'[{delimiters}]', fts))
        query = basedata_helper.bd_helper.BDHelper.get_items(
            bd_connection, cls.TABLE_NAME, None, f"""fts LIKE '%{fts.lower()}%'""", limit=limit, offset=offset,
            sorted_headers=cls.PRIMARY_KEYS, reverse=False)
        return {
            f"{cls.TABLE_NAME}_list": [dict(zip(cls.KEYS, item)) for item in query],
            "pages_count": basedata_helper.bd_helper.BDHelper.get_page_count(
                bd_connection, cls.TABLE_NAME, f"""fts LIKE '%{fts.lower()}%'""", limit)
        }

    @classmethod
    def get_by_genre(cls, bd_connection, genre: int, limit: int = -1, offset: int = 0):
        query = basedata_helper.bd_helper.BDHelper.get_items(
            bd_connection, cls.TABLE_NAME, None, f"""(genres & {genre}) = {genre}""", limit=limit, offset=offset,
            sorted_headers=cls.PRIMARY_KEYS, reverse=False)
        return {
            f"{cls.TABLE_NAME}_list": [dict(zip(cls.KEYS, item)) for item in query],
            "pages_count": basedata_helper.bd_helper.BDHelper.get_page_count(
                bd_connection, cls.TABLE_NAME,  f"""(genres & {genre}) = {genre}""", limit)
        }

    @classmethod
    def get_sorted_by_time(cls, bd_connection, limit: int = -1, offset: int = 0, reverse=False):
        query = basedata_helper.bd_helper.BDHelper.get_items(
            bd_connection, cls.TABLE_NAME, None, None, limit=limit, offset=offset,
            sorted_headers=["added_datatime"], reverse=reverse)
        if query:
            return {
                f"{cls.TABLE_NAME}_list": [dict(zip(cls.KEYS, item)) for item in query],
                "pages_count": basedata_helper.bd_helper.BDHelper.get_page_count(
                    bd_connection, cls.TABLE_NAME, None, limit)
            }
        return None

    @classmethod
    def get_updates_by_chapters(cls, limit: int = -1, offset: int = 0):
        pass


if __name__ == "__main__":
    bd = sqlite3.connect("basedata_test.db")
    # print("\n", "=" * 3, "---   Test BDUser.added_values()   ---", "=" * 3, sep="")
    # pprint.pprint(BDWork.append_item(bd, {
    #     "id_work": "Gabriel_Dropout_Shcool",
    #     "id_user": 1,
    #     "id_preview_image": 541,
    #     "rus_name": "Габриель бросает школу",
    #     "eng_name": "Gabriel Dropout Shcool",
    #     "description":
    #         """Габриэль Тэнма Уайт была одной из самых прилежных учениц Академии Ангелов.
    #          Но вот пришло время выпуска, и Габриэль отправилась на Землю, чтобы выполнить
    #           порученную ей миссию - показать людям правильный путь и подарить им счастье.
    #            Однако действительно ли всё будет именно так? Не изменит ли ангела новое место,
    #             в которое она попала?..""",
    #     "genres": 13378
    # }))
    # print("\n", "=" * 3, "---   Test BDUser.get_all()   ---", "=" * 3, sep="")
    # pprint.pprint(BDWork.get_all(bd, limit=2))
    print("\n", "=" * 3, "---   Test BDUser.get_by_primary_keys_dict()   ---", "=" * 3, sep="")
    pprint.pprint(BDWork.get_by_primary_keys_dict(bd, {"id_work": "Mandy"}))
    print("\n", "=" * 3, "---   Test BDUser.get_by_primary_keys()   ---", "=" * 3, sep="")
    pprint.pprint(BDWork.ft_search_work(bd, "человек-паук"))
    print("\n", "=" * 3, "---   Test BDUser.get_by_genre()   ---", "=" * 3, sep="")
    pprint.pprint(BDWork.get_by_genre(bd, 8192))
    print("\n", "=" * 3, "---   Test BDUser.get_sorted_by_time()   ---", "=" * 3, sep="")
    pprint.pprint(BDWork.get_sorted_by_time(bd, limit=2))
    # print("\n", "=" * 3, "---   Test BDUser.delete_item()   ---", "=" * 3, sep="")
    # pprint.pprint(BDWork.delete_item(bd, {"id_work": "Gabriel_Dropout_Shcool"}))
