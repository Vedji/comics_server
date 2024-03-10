import pprint
import sqlite3
import basedata_helper.bd_unit


class BDFile(basedata_helper.bd_unit.BDUnit):
    PRIMARY_KEYS = ["image_id"]
    KEYS = ["image_id", "image_path", "image_name", "image_format"]
    TABLE_NAME = "files"


if __name__ == "__main__":
    bd = sqlite3.connect("basedata_test.db")
    print("\n", "=" * 3, "---   Test BDFile.get_all()   ---", "=" * 3, sep="")
    pprint.pprint(BDFile.get_by_primary_keys(bd, {"image_id": 18}))
    bd = sqlite3.connect("basedata_test.db")
    print("\n", "=" * 3, "---   Test BDFile.get_all()   ---", "=" * 3, sep="")
    pprint.pprint(BDFile.get_all(bd, limit=5))
    print("\n", "=" * 3, "---   Test BDFile.append_item()   ---", "=" * 3, sep="")
    file = BDFile.append_item(bd, {"image_path": "test/manga", "image_name": "test.png", "image_format": "png"})
    pprint.pprint(file)
    print("\n", "=" * 3, "---   Test BDFile.delete_item()   ---", "=" * 3, sep="")
    pprint.pprint(BDFile.delete_item(bd, {"image_id": file["image_id"]}))
