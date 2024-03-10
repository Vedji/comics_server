import datetime
import pprint
import sqlite3
import basedata_helper.bd_unit


class BDChapter(basedata_helper.bd_unit.BDUnit):
    PRIMARY_KEYS = ["id_work", "number_chapter"]
    KEYS = ["id_work", "id_user", "number_chapter", "added_datatime", "name", "length"]
    TABLE_NAME = "chapters"

    @classmethod
    def append_item(cls, bd_connection: sqlite3.Connection, added_values: dict) -> dict | None:
        if "added_datatime" not in added_values:
            added_values = {**added_values, "added_datatime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        return super().append_item(bd_connection, added_values)


if __name__ == "__main__":
    bd = sqlite3.connect("basedata_test.db")
    print("\n", "="*3, "---   Test BDChapter.get_all()   ---", "="*3, sep="")
    pprint.pprint(BDChapter.get_all(bd, limit=2))
    print("\n", "=" * 3, "---   Test BDChapter.get_by_primary_keys()   ---", "=" * 3, sep="")
    pprint.pprint(BDChapter.get_by_primary_keys(bd, {"id_work": 'Mandy', "number_chapter": '3'}))
    print("\n", "=" * 3, "---   Test BDChapter.append_item()   ---", "=" * 3, sep="")
    pprint.pprint(BDChapter.append_item(bd, {
        'id_user': 1,
        'id_work': 'Mandy',
        'length': 400,
        'name': 'Test',
        'number_chapter': 4
    }))
    print("\n", "=" * 3, "---   Test BDChapter.get_all()   ---", "=" * 3, sep="")
    pprint.pprint(BDChapter.get_all(bd))
    print("\n", "=" * 3, "---   Test BDChapter.update_item()   ---", "=" * 3, sep="")
    pprint.pprint(BDChapter.update_item(bd, {'id_work': 'Mandy', 'number_chapter': 4}, {"length": 999999}))
    print("\n", "=" * 3, "---   Test BDChapter.get_all()   ---", "=" * 3, sep="")
    pprint.pprint(BDChapter.get_all(bd))
    print("\n", "=" * 3, "---   Test BDChapter.delete_item()   ---", "=" * 3, sep="")
    pprint.pprint(BDChapter.delete_item(bd, {'id_work': 'Mandy', 'number_chapter': 4}))
    print("\n", "=" * 3, "---   Test BDChapter.get_all()   ---", "=" * 3, sep="")
    pprint.pprint(BDChapter.get_all(bd))
