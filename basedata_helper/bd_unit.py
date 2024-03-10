import pprint
import sqlite3
import basedata_helper.bd_helper


class BDUnit:
    PRIMARY_KEYS = None
    KEYS = None
    TABLE_NAME = None

    @classmethod
    def _checker_init(cls):
        if cls.TABLE_NAME is None or cls.KEYS is None or cls.PRIMARY_KEYS is None:
            raise KeyError(f"Class {cls.__name__} has not initialization.")

    @classmethod
    def _checker_primary_keys(cls, pk: dict):
        invalid_keys = list(filter(lambda x: x not in cls.PRIMARY_KEYS, pk.keys()))
        if len(invalid_keys) > 0:
            raise KeyError(f" In class: {cls.__name__} not PRIMARY KEYS {', '.join(invalid_keys)};")

    @classmethod
    def _checker_keys(cls, keys: dict):
        invalid_keys = list(filter(lambda x: x not in cls.KEYS, keys.keys()))
        if len(invalid_keys) > 0:
            raise KeyError(f" In class: {cls.__name__} not KEYS {', '.join(invalid_keys)};")

    @classmethod
    def get_all(cls, bd_connection: sqlite3.Connection, limit: int = -1, offset: int = 0) -> dict | None:
        cls._checker_init()
        query = basedata_helper.bd_helper.BDHelper.get_items(
            bd_connection,
            cls.TABLE_NAME, None, None, limit=limit, offset=offset, sorted_headers=cls.PRIMARY_KEYS, reverse=False
        )
        if query:
            return {
                f"{cls.TABLE_NAME}_list": [dict(zip(cls.KEYS, query[i])) for i in range(len(query))],
                "pages_count":
                    basedata_helper.bd_helper.BDHelper.get_page_count(bd_connection, cls.TABLE_NAME, None, limit)
            }
        return None

    @classmethod
    def get_by_primary_keys_dict(cls, bd_connection: sqlite3.Connection, pk: dict) -> dict | None:
        cls._checker_init()
        cls._checker_primary_keys(pk)
        query = basedata_helper.bd_helper.BDHelper.get_item(
            bd_connection, cls.TABLE_NAME, None, " AND ".join([f"\"{key}\" = '{val}'" for key, val in pk.items()]))
        return dict(zip(cls.KEYS, query))

    @classmethod
    def get_by_id(cls, **kwargs):
        pass

    @classmethod
    def append_item(
            cls,
            bd_connection: sqlite3.Connection,
            added_values: dict
    ) -> dict | None:
        cls._checker_init()
        cls._checker_keys(added_values)
        query = basedata_helper.bd_helper.BDHelper.add_element(bd_connection, cls.TABLE_NAME, added_values)
        if query:
            return dict(zip(cls.KEYS, query))
        return None

    @classmethod
    def update_item(
            cls,
            bd_connection: sqlite3.Connection,
            pk: dict,
            updated_values: dict
    ) -> dict | None:
        cls._checker_init()
        cls._checker_primary_keys(pk)
        cls._checker_keys({**pk, **updated_values})
        query = basedata_helper.bd_helper.BDHelper.update_element(bd_connection, cls.TABLE_NAME, updated_values, pk)
        if query:
            return dict(zip(cls.KEYS, query))
        return None

    @classmethod
    def delete_item(cls, bd_connection: sqlite3.Connection, pk: dict) -> dict | None:
        cls._checker_init()
        cls._checker_primary_keys(pk)
        if not all(map(lambda x: x in cls.PRIMARY_KEYS, pk.keys())):
            raise KeyError(f" In class: {cls.__name__} keys: {', '.join(pk.keys())} != {', '.join(cls.PRIMARY_KEYS)};")
        query = basedata_helper.bd_helper.BDHelper.del_element(bd_connection, cls.TABLE_NAME, pk)
        if query:
            return dict(zip(cls.KEYS, query))
        return None


