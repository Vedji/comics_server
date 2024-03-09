"""

    {
        "request": "test",
        "request_type": "GET",
        "type_output": " JSON || None",
        "request_desc": "Request description text example",
        "argument_desc": " * arg1: str - example",
        "example_output": "{arg2: 'one'}",
        "request_example": " * arg2: bool"
    },
    {
        "request": "",
        "request_type": "GET",
        "type_output": " JSON || None",
        "request_desc": "",
        "argument_desc": "",
        "example_output": "",
        "request_example": "",
    },

"""


api_desc = [
    {
        "request": "/api_v2/get_status/server",
        "request_type": "GET",
        "type_output": " JSON || None",
        "request_desc": "Возвращает статус сервера",
        "argument_desc": " None ",
        "example_output": "{ server_status: bool }",
        "request_example": "* server_status: bool - Статус сервера",
    },
    {
        "request": "/api_v2/get_info/file",
        "request_type": "GET",
        "type_output": " JSON || None",
        "request_desc": "Возвращает id изображения, которая содержится в манге, в n главе, на k странице ",
        "argument_desc": "* manga_name: str - название манги в БД;\n * chapter_number: int - номер главы;\n"
                         " * page_number: int - номер страницы в главе;",
        "example_output": "{ id_page_image: str }",
        "request_example": "* id_page_image - id файла",
    },
    {
        "request": "/api_v2/get_info/chapter",
        "request_type": "GET",
        "type_output": " JSON || None",
        "request_desc": "Возвращает информацию о главе манги, по ее номеру: название главы, кол-во страниц в главе",
        "argument_desc": "manga_name: str - название манги в БД; chapter_number: int - номер главы;",
        "example_output": "{ chapter_name: str, chapter_len: int }",
        "request_example": "* chapter_name - название главы\n * chapter_len - количество страниц в главе",
    },
    {
        "request": "/api_v2/get_list/manga_name",
        "request_type": "GET",
        "type_output": " JSON || None",
        "request_desc": "Возвращает список названий манг в виде list,"
                        " в параметре list_manga_name. В случае неудачи None.",
        "argument_desc": "* limit: int - ограничение на количество;\n * offset: int - смещение при получении значений",
        "example_output": "{ list_manga_name: list[str] }",
        "request_example": "* list_manga_name - список названий манг",
    },
    {
        "request": "/api_v2/get_list/manga_chapters",
        "request_type": "GET",
        "type_output": " JSON || None",
        "request_desc": "Возвращает список глав, манги по ее названию, где chapter_number - номер главы,"
                        " chapter_name - название, chapter_len - кол-во страниц в главе",
        "argument_desc": "manga_name: str - название манги в БД",
        "example_output": "{\n\t list_manga_chapters: list[dict]"
                          "\t{ \n\t\tchapter_number: int,\n\t\tchapter_name: str,\n\t\tchapter_len: int \n\t} \n }",
        "request_example": "* list_manga_chapters - список глав манги, в котором элементы представляются в виде:\n"
                           "\t * chapter_number - номер главы\n\t * chapter_name - название главы\n"
                           "\t * chapter_len - количество страниц в главе",
    },
    {
        "request": "/api_v2/get_file",
        "request_type": "GET",
        "type_output": " File || None",
        "request_desc": "Возвращает файл для скачивания или отображения",
        "argument_desc": "manga_name: str - название манги в БД",
        "example_output": "	--- ",
        "request_example": " Возвращает файл ( Изображение )",
    },
    {
        "request": "/api_v2/get_len/chapter",
        "request_type": "GET",
        "type_output": " JSON || None",
        "request_desc": "Возвращает длинну отдельной главы, манги.",
        "argument_desc": "* manga_name: str - название манги в БД;\n * chapter_number: int - номер главы",
        "example_output": "{ 'len': int }",
        "request_example": "len - количество страниц в главе манги",
    },

]
