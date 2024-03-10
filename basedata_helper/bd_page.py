import pprint
import sqlite3
import basedata_helper.bd_unit


class BDPage(basedata_helper.bd_unit.BDUnit):
    PRIMARY_KEYS = ["id_work", "number_chapter", "number_page"]
    KEYS = ["id_work", "number_chapter", "number_page", "page_image"]
    TABLE_NAME = "pages"


if __name__ == "__main__":
    bd = sqlite3.connect("basedata_test.db")
    print("\n", "=" * 3, "---   Test BDPage.get_by_primary_keys()   ---", "=" * 3, sep="")
    pprint.pprint(BDPage.get_by_primary_keys(bd, {"id_work": "Mandy", "number_chapter": 0, "number_page": 7}))
    bd = sqlite3.connect("basedata_test.db")
    print("\n", "=" * 3, "---   Test BDPage.get_all()   ---", "=" * 3, sep="")
    pprint.pprint(BDPage.get_all(bd))
