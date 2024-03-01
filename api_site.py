import flask
from flask import request, jsonify, send_file
import bd_connect


def get_manga_genre(line: str):
    genres = [
        "Романтика", "Драма", "Комедия", "Фэнтези", "Приключения", "Повседневность", "Киберпанк", "Психологическое",
        "Космос", "Магия", "Фантастика", "Пост-апокалипсис", "Боевик", "Меха", "Сверхъестественное", "Детектив"
    ]
    if len(line) != len(genres):
        return ["Error"]
    return list(filter(lambda x: x is not None, [genres[i] if line[i] == "1" else None for i in range(len(line))]))


def init_site_api(app: flask.app.Flask, get_db):
    @app.route("/api/bd/get_list", methods=["POST"])
    def api_bd_get():
        if "table_name" not in request.json or "limit" not in request.json or "offset" not in request.json:
            return jsonify({"result": False})
        result = bd_connect.BDConnect.get_bd_page(
            get_db(), request.json["table_name"],
            request.json["offset"],
            request.json["limit"]
        )
        result["result"] = True
        return jsonify(result)

    @app.route('/api/user/registration', methods=["POST"])
    def api_user_reg():
        if "user_login" not in request.json or "user_password" not in request.json:
            return jsonify({"result": False})
        if not bd_connect.BDConnect.is_user(get_db(), request.json["user_login"]) \
                and len(request.json["user_password"]) > 6:
            bd_connect.BDConnect.user_registration(get_db(), request.json["user_login"], request.json["user_password"])
            return jsonify({"result": True, "is_user_reg": True})
        return jsonify({"result": True, "is_user_reg": False})


    @app.route("/api/user/user_info", methods=["POST"])
    def api_user_user_info():
        if "user_password" not in request.json or "user_login" not in request.json:
            return jsonify({"result": False})
        data = bd_connect.BDConnect.api_get_user_info(
            get_db(), request.json["user_login"]
        )
        result = {"result": False}
        print(data)
        if (data["result"] and data["user_name"] == request.json["user_login"] and
                request.json["user_password"] == data["user_password"]):
            result["result"] = True
            result["user_id"] = data["user_id"]
            result["user_name"] = data["user_name"]
            result["role"] = data["role"]
        return jsonify(result)

    @app.route("/api/user/user_read_list", methods=["POST"])
    def api_user_user_read_list():
        if "user_password" not in request.json or "user_login" not in request.json:
            return jsonify({"result": False})
        data = bd_connect.BDConnect.api_get_user_info(
            get_db(), request.json["user_login"]
        )
        result = {"result": False}
        print(data)
        if (data["result"] and data["user_name"] == request.json["user_login"] and
                request.json["user_password"] == data["user_password"]):
            result["result"] = True
            result["user_id"] = data["user_id"]
            result["user_name"] = data["user_name"]
            result["role"] = data["role"]
        return jsonify(result)

    @app.route("/api/catalog/info", methods=["GET"])
    def api_catalog_info():
        manga_name = request.args.get("name")
        data = bd_connect.BDConnect.get_info_manga(get_db(), manga_name)
        result = {"result": False}
        if data:
            result = data
            data["result"] = True
        return jsonify(result)

    @app.route("/api/catalog/chapters", methods=["GET"])
    def api_catalog_manga_info():
        manga_name = request.args.get("name")
        data = bd_connect.BDConnect.get_list_manga_chapters(get_db(), manga_name)
        result = {"result": False}
        if data:
            result = data
            data["result"] = True
            print(data)
        return jsonify(result)

    @app.route("/api/catalog/manga/chapter", methods=["GET"])
    def api_catalog_manga_chapter():
        result = {"result": False}
        manga_name = request.args.get("name")
        try:
            chapter = int(request.args.get("c"))
        except ValueError:
            return jsonify(result)
        data = bd_connect.BDConnect.get_info_chapter(get_db(), manga_name, chapter)
        if data:
            result = data
            result["result"] = True
        return jsonify(result)

    @app.route("/api/catalog/manga/page", methods=["GET"])
    def api_catalog_manga_page():
        manga_name = request.args.get("name")
        chapter_number = request.args.get("c")
        page_number = request.args.get("p")
        result = {"result": False}
        try:
            chapter_number = int(chapter_number) if chapter_number and chapter_number.isdigit() else -1
            page_number = int(page_number) if page_number and page_number.isdigit() else -1
        except ValueError:
            return jsonify(result)
        data = bd_connect.BDConnect.get_info_page(get_db(), manga_name, chapter_number, page_number)
        if data:
            result = data
            result["result"] = True
        return jsonify(result)

    @app.route("/api/catalog/manga/comments", methods=["GET"])
    def api_catalog_manga_comments():
        manga_name = request.args.get("name")
        offset = request.args.get("offset")
        limit = request.args.get("limit")
        result = {"result": False}
        try:
            offset = int(offset) if offset and offset.isdigit() else 0
            limit = int(limit) if limit and limit.isdigit() else -1
        except ValueError:
            return jsonify(result)
        data = bd_connect.BDConnect.api_get_manga_comments(get_db(), manga_name, limit, offset)
        if data and "comments" in data:
            result = data
            result["result"] = True
        return jsonify(result)

    @app.route("/api/catalog/manga/is_read", methods=["POST"])
    def api_catalog_manga_is_read():
        result = {"result": False}
        if "user_password" not in request.json or "user_login" not in request.json or "manga_name" not in request.json:
            return jsonify(result)
        data = bd_connect.BDConnect.manga_in_likes_list(
            get_db(),
            request.json["user_login"], request.json["user_password"], request.json["manga_name"])
        if data and "manga_in_user_manga_like_list" in data:
            result = data
            result["result"] = True
        return jsonify(result)

    @app.route("/api/catalog/manga/set_read", methods=["POST"])
    def api_catalog_manga_set_manga():
        result = {"result": False}
        if "user_password" not in request.json or "user_login" not in request.json or "manga_name" not in request.json:
            return jsonify(result)
        data = bd_connect.BDConnect.add_manga_in_like_manga_user(
            get_db(),
            request.json["user_login"], request.json["user_password"], request.json["manga_name"])
        if data and "manga_in_user_like_manga" in data:
            result = data
            result["result"] = True
        return jsonify(result)

    @app.route("/api/user/del_comment", methods=["POST"])
    def api_user_del_comment():
        result = {"result": False}
        if "user_password" not in request.json or "user_login" not in request.json or "manga_name" not in request.json:
            return jsonify(result)
        data = bd_connect.BDConnect.delete_user_comment(
            get_db(),
            request.json["user_login"], request.json["user_password"], request.json["manga_name"])
        if data and "commit" in data and data["commit"]:
            result["result"] = True
        return jsonify(result)

    @app.route("/api/user/read_list/get", methods=["POST"])
    def api_user_read_list_get():
        result = {"result": False}
        if ("user_password" not in request.json or "user_login" not in request.json
                or "limit" not in request.json or "offset" not in request.json):
            return jsonify(result)
        try:
            user_login = request.json["user_login"]
            user_password = request.json["user_password"]
            offset = request.json["offset"]
            limit = request.json["limit"]
        except ValueError:
            return jsonify(result)
        data = bd_connect.BDConnect.get_user_read_catalog_list(
            get_db(),
            user_login, user_password, limit, offset)
        if data and "read_manga_list" in data:
            result = data
            result["result"] = True
        return jsonify(result)

    @app.route("/api/user/comment_list/get", methods=["POST"])
    def api_user_comments_list_get():
        result = {"result": False}
        if ("user_password" not in request.json or "user_login" not in request.json
                or "limit" not in request.json or "offset" not in request.json):
            return jsonify(result)
        try:
            user_login = request.json["user_login"]
            user_password = request.json["user_password"]
            offset = request.json["offset"]
            limit = request.json["limit"]
        except ValueError:
            return jsonify(result)
        data = bd_connect.BDConnect.get_user_comments(
            get_db(),
            user_login, user_password, limit, offset)
        if data and "comments" in data:
            result = data
            result["result"] = True
        return jsonify(result)

    @app.route("/api/user/replace_password", methods=["POST"])
    def api_user_replaace_password():
        result = {"result": False}
        if "user_password" not in request.json or "user_login" not in request.json or "manga_name" not in request.json:
            return jsonify(result)
        data = bd_connect.BDConnect.add_manga_in_like_manga_user(
            get_db(),
            request.json["user_login"], request.json["user_password"], request.json["manga_name"])
        if data and "manga_in_user_like_manga" in data:
            result = data
            result["result"] = True
        return jsonify(result)

    @app.route("/api/manga/get_catalog", methods=["POST"])
    def api_manga_get_catalog():
        """ Принимает параметры limit, offset и template, возвращает список манги по заданным параметрам """
        if "limit" not in request.json or "offset" not in request.json:
            return jsonify({"result": False})
        if "template" not in request.json:
            result = bd_connect.BDConnect.get_catalog_manga(
                get_db(), request.json["offset"], request.json["limit"])
        else:
            result = bd_connect.BDConnect.get_catalog_manga(
                get_db(), request.json["offset"], request.json["limit"], request.json["template"])
        result["result"] = True
        return jsonify(result)

    @app.route("/api/file_upload", methods=["POST"])
    def upload_file():
        if 'file' not in request.files:
            return {"result": False, "Error_type": 0}
        if "manga_name" not in request.json:
            return {"result": False, "Error_type": 1}
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            file.save('uploads/' + file.filename)  # Путь к папке, куда будут сохраняться загруженные файлы
            return 'File uploaded successfully'





