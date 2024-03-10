import sqlite3
import unittest
from bd_work import BDWork


class TestBDHelper(unittest.TestCase):
    def __init__(self, method_name):
        super().__init__(method_name)
        self.bd = sqlite3.connect("basedata_test.db")

    def test_user_authorization(self):
        work_added: dict = BDWork.append_item(
            self.bd,
            {
                "id_work": "Gabriel_Dropout_Shcool_test",
                "id_user": 1,
                "id_preview_image": 541,
                "rus_name": "Габриель бросает школу",
                "eng_name": "Gabriel Dropout Shcool",
                "description":
                    """Габриэль Тэнма Уайт была одной из самых прилежных учениц Академии Ангелов.
                     Но вот пришло время выпуска, и Габриэль отправилась на Землю, чтобы выполнить
                      порученную ей миссию - показать людям правильный путь и подарить им счастье.
                       Однако действительно ли всё будет именно так? Не изменит ли ангела новое место,
                        в которое она попала?..""",
                "genres": 13378
            }
        )
        self.assertEqual(BDWork.get_by_primary_keys_dict(self.bd, {"id_work": "Gabriel_Dropout_Shcool_test"}), work_added)
        self.assertEqual(BDWork.delete_item(self.bd, {"id_work": "Gabriel_Dropout_Shcool_test"}), work_added)


if __name__ == "__main__":
    unittest.main()
