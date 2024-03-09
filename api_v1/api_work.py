import flask
from flask import request, jsonify
import os
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.datastructures import FileStorage
import api_v1.exception
import api_v1.genre_template
import api_v1.bd_connect


def init_site_api(app: flask.app.Flask, get_db):
    html_split_symbol = '+'

    @app.route('/api/v1/work', methods=["GET"])
    def api_works_catalog():
        """ Get a list of works """
        limit = -1
        offset = 0
        search_name = None
        genre = None
        limit, msg, _terr = api_v1.exception.get_arg(request.args.get("limit"), lambda x: int(x), "limit", -1)
        if msg["status"] == "error" and _terr is not TypeError:
            return jsonify(msg), msg["code"]
        offset, msg, _terr = api_v1.exception.get_arg(request.args.get("offset"), lambda x: int(x), "offset", 0)
        if msg["status"] == "error" and _terr is not TypeError:
            return jsonify(msg), msg["code"]
        if request.args.get("genre") and len(request.args.get("genre")) > 0:
            if not api_v1.genre_template.Genre.check_temp(request.args.get("genre")):
                return jsonify({"status": "error", "code": 400, "message": "Argument genre is not a correct"}), 400
            genre = request.args.get("genre")
        if request.args.get("search_name") and len(request.args.get("search_name")) > 0:
            search_name = request.args.get("search_name").replace(html_split_symbol, " ", -1)
        return jsonify({
            "status": "success",
            "data": api_v1.bd_connect.BDConnect.get_works_catalog(get_db(), limit, offset, genre, search_name)
        }), 200

    @app.route('/api/v1/work', methods=["POST"])
    @jwt_required()
    def api_add_work():
        """ Add a new work """
        user_data = get_jwt()
        per = user_data["ROLE"]
        pre_img = request.files.get("pre_img", None)
        work_id = request.form.get("work_id", None, str)
        ru_name = request.form.get("ru_name", None, str)
        desc = request.form.get("desc", "", str)
        genre = request.form.get("genre", "", str)

        if per > 2 or per < 1:
            return jsonify({"status": "error", "code": 401, "message": "No Permission"}), 401
        if pre_img is None or type(pre_img) is not FileStorage:
            return jsonify({"status": "error", "code": 400, "message": "Argument pre_img is not exists"}), 400
        if work_id is None or len(work_id) < 1:
            return jsonify({"status": "error", "code": 400, "message": "Argument work_id is not exists"}), 400
        if ru_name is None or len(ru_name) < 1:
            return jsonify({"status": "error", "code": 400, "message": "Argument ru_name is not exists"}), 400
        if desc is None or len(desc) < 1:
            return jsonify({"status": "error", "code": 400, "message": "Argument desc is not exists"}), 400
        if genre is None or len(genre) < 1:
            return jsonify({"status": "error", "code": 400, "message": "Argument genre is not exists"}), 400
        if work_id == '_' or not api_v1.genre_template.Genre.is_english_alphabet(work_id):
            return jsonify({"status": "error", "code": 400, "message": "Id's is not on english and symbols '_' "}), 400
        if api_v1.bd_connect.BDConnect.is_work_id_exists(get_db(), work_id):
            return jsonify({"status": "error", "code": 400, "message": "Is this work is already exists"}), 400
        if os.path.exists("/".join(["manga", work_id])):
            return jsonify({"status": "error", "code": 400, "message": "Is work directory is already exists"}), 400
        # All checkers end
        if api_v1.bd_connect.BDConnect.add_work(
            get_db(),
            work_id,
            ru_name,
            desc,
            genre,
            pre_img
        ):
            return jsonify({"status": "success", "data": {}}), 200
        else:
            return jsonify({"status": "error", "code": 400, "message": "Error on upload "}), 400

    @app.route('/api/v1/work/<work_id>', methods=["GET"])
    def api_get_work(work_id: str):
        """ Return information about the work """
        if type(work_id) is not str or len(work_id) <= 0:
            return jsonify({"status": "error", "code": 400, "message": "Argument work_id is not exists"}), 400
        data = api_v1.bd_connect.BDConnect.get_work(get_db(), work_id)
        if data:
            data["genre_headers"] = api_v1.genre_template.Genre.get_manga_genre(data["genre"])
            return jsonify({"status": "success", "data": data}), 200
        return jsonify({"status": "error", "code": 404, "message": f"Work '{work_id}' not found"}), 404

    @app.route('/api/v1/work/<work_id>/chapter', methods=["GET"])
    def api_get_work_chapters(work_id: str):
        """ Return a list of chapters of a work """
        data = api_v1.bd_connect.BDConnect.get_work_chapters(get_db(), work_id)
        if data is not None:
            return jsonify({
                "status": "success",
                "data": {
                    "id": work_id,
                    "chapters_list": data
                }
            }), 200
        return jsonify({"status": "error", "code": 404, "message": f"Work '{work_id}' not found"}), 404

    @app.route('/api/v1/work/<work_id>/chapter', methods=["POST"])
    @jwt_required()
    def api_add_work_chapter_catalog(work_id: str):
        user_data = get_jwt()
        per = user_data["ROLE"]

        chapter_name = request.form.get("chapter_name", None, str)
        chapter_num = request.form.get("chapter_num", -1, int)
        count_files = request.form.get("count_files", 0, int)
        files = []

        if per > 2 or per < 1:
            return jsonify({"status": "error", "code": 401, "message": "No Permission"}), 401
        if type(work_id) is not str:
            return jsonify({"status": "error", "code": 400, "message": "Argument work_id is not exists"}), 400
        if len(work_id) < 1:
            return jsonify({"status": "error", "code": 400, "message": "Argument work_id too small"}), 400
        if chapter_name is None:
            return jsonify({"status": "error", "code": 400, "message": "Argument chapter_name is not exists"}), 400
        if chapter_num < 0:
            return jsonify({"status": "error", "code": 400, "message": "Argument chapter_num is not exists"}), 400
        if count_files < 1:
            return jsonify({"status": "error", "code": 400, "message": "Argument count_files is not exists"}), 400
        if not api_v1.bd_connect.BDConnect.is_work_id_exists(get_db(), work_id):
            return jsonify({"status": "error", "code": 400, "message": "Argument work is not exists"}), 400
        for i in range(int(count_files)):
            if f"file_{i}" not in request.files or request.files[f"file_{i}"].filename.split('.')[-1] != "jpg":
                return jsonify({"status": "error", "code": 400, "message": f"Argument file_{i} is not exists"}), 400
            files.append(request.files[f"file_{i}"])
        if len(chapter_name) == 0:
            chapter_name = f"Глава {request.form['chapter_num']}"
        if api_v1.bd_connect.BDConnect.work_chapter_exists(get_db(), work_id, chapter_num):
            return jsonify({"status": "error", "code": 400, "message": "Chapter already exists"}), 400
        if not api_v1.bd_connect.BDConnect.add_work_chapter(
                get_db(), work_id, chapter_name, int(chapter_num), files):
            return jsonify({"status": "error", "code": 400, "message": "Just error"}), 400
        return jsonify({"status": "success", "data": {}}), 200

    @app.route('/api/v1/work/<work_id>/chapter/<c_num>', methods=["GET"])
    def api_get_work_chapter(work_id: str, c_num: int) -> dict:
        """ Return info about work chapter """
        pass

    @app.route('/api/v1/work/<work_id>/chapter/<c_num>/page', methods=["GET"])
    def api_get_work_chapter_pages_list(work_id: str, c_num: int) -> dict:
        """ Return a list of pages of a work """
        pass

    @app.route('/api/v1/work/<work_id>/chapter/<c_num>/page/<p_num>', methods=["GET"])
    def api_get_work_chapter_page(work_id: str, c_num: int, p_num: int) -> dict:
        """ Return info about work chapter page """
        pass

    @app.route('/api/v1/work/<work_id>/comments', methods=["GET"])
    def api_get_work_comments(work_id: str):
        """ Return info about work chapter """
        limit = request.args.get("limit", -1, int)
        offset = request.args.get("offset", 0, int)
        but_user = request.args.get("but_user_id", None, int)
        data = api_v1.bd_connect.BDConnect.get_work_comments_list(get_db(), work_id, limit, offset, but_user)
        if data is None:
            return jsonify({"status": "error", "code": 404, "message": f"Work {work_id} not found"}), 404
        return jsonify({
            "status": "success",
            "data": data
        }), 200

    @app.route('/api/v1/work/<work_id>/rating', methods=["GET"])
    def api_get_work_rating(work_id: str):
        """ Return avg-rating work chapter """
        data, msg, _terr = api_v1.exception.req_fun(
            lambda: api_v1.bd_connect.BDConnect.get_awg_rating_work(get_db(), work_id), default=0)
        if msg["status"] == "error":
            return jsonify(msg), msg["code"]
        return jsonify({
            "status": "success",
            "data": {
                "rating_average": data
            }
        }), 200

    @app.route('/api/v1/work/<work_id>', methods=["DELETE"])
    @jwt_required()
    def api_del_work(work_id: str):
        user_data = get_jwt()
        per = user_data["ROLE"]
        if per > 2 or per < 1:
            return jsonify({"status": "error", "code": 401, "message": "No Permission"}), 401
        api_v1.bd_connect.BDConnect.del_work(get_db(), work_id)
        return jsonify({"status": "success", "data": {}}), 200
