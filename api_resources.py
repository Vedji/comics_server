import pprint

import flask
from flask import request, jsonify, send_file
import bd_connect
import os
import genre_template


def init_site_api(app: flask.app.Flask, get_db):

    @app.route('/api/resources/add_work', methods=["POST"])
    def api_resources_add_work():
        if 'login' not in request.form or 'password' not in request.form:
            return {"status": "error", "code": 401, "message": "No authorization"}
        if not bd_connect.BDConnect.is_user_authorization(get_db(), request.form["login"], request.form["password"]):
            return {"status": "error", "code": 401, "message": "No authorization"}
        per = bd_connect.BDConnect.get_user_permission_level(get_db(), request.form["login"], request.form["password"])
        if per > 2 or per < 1:
            return {"status": "error", "code": 401, "message": "No Permission"}
        if 'pre_img' not in request.files:
            return {"status": "error", "code": 400, "message": "Argument pre_img is not exists"}
        if 'id' not in request.form:
            return {"status": "error", "code": 400, "message": "Argument id is not exists"}
        if 'ru_name' not in request.form:
            return {"status": "error", "code": 400, "message": "Argument ru_name is not exists"}
        if 'desc' not in request.form:
            return {"status": "error", "code": 400, "message": "Argument desc is not exists"}
        if 'genre' not in request.form:
            return {"status": "error", "code": 400, "message": "Argument genre is not exists"}
        if request.form["id"][0] == '_' or not genre_template.Genre.is_english_alphabet(request.form["id"]):
            return {"status": "error", "code": 400, "message": "Id's is not on english and symbols '_' "}
        if bd_connect.BDConnect.is_work_id_exists(get_db(), request.form["id"]):
            return {"status": "error", "code": 400, "message": "Is this work is already exists"}
        if os.path.exists("/".join(["manga", request.form["id"]])):
            return {"status": "error", "code": 400, "message": "Is work directory is already exists"}
        # All checkers end
        if bd_connect.BDConnect.add_work(
            get_db(),
            request.form["id"],
            request.form["ru_name"],
            request.form["desc"],
            request.form["genre"],
            request.files["pre_img"]
        ):
            return {"status": "success", "data": {}}
        else:
            return {"status": "error", "code": 400, "message": "Error on upload "}

    @app.route('/api/resources/add_work_chapter', methods=["POST"])
    def api_resources_add_work_chapter():
        chapter_name = request.form["chapter_name"]
        files = []
        if 'login' not in request.form or 'password' not in request.form:
            return {"status": "error", "code": 401, "message": "No authorization"}
        if not bd_connect.BDConnect.is_user_authorization(get_db(), request.form["login"], request.form["password"]):
            return {"status": "error", "code": 401, "message": "No authorization"}
        per = bd_connect.BDConnect.get_user_permission_level(get_db(), request.form["login"], request.form["password"])
        if per > 2 or per < 1:
            return {"status": "error", "code": 401, "message": "No Permission"}
        if 'id' not in request.form:
            return {"status": "error", "code": 400, "message": "Argument id is not exists"}
        if 'chapter_name' not in request.form:
            return {"status": "error", "code": 400, "message": "Argument chapter_name is not exists"}
        if 'chapter_num' not in request.form or not request.form["chapter_num"].isdigit():
            return {"status": "error", "code": 400, "message": "Argument chapter_num is not exists"}
        if 'count_files' not in request.form or not request.form["count_files"].isdigit():
            return {"status": "error", "code": 400, "message": "Argument count_files is not exists"}
        if not bd_connect.BDConnect.is_work_id_exists(get_db(), request.form["id"]):
            return {"status": "error", "code": 400, "message": "Argument work is not exists"}
        for i in range(int(request.form["count_files"])):
            if f"file_{i}" not in request.files or request.files[f"file_{i}"].filename.split('.')[-1] != "jpg":
                return {"status": "error", "code": 400, "message": f"Argument file_{i} is not exists"}
            files.append(request.files[f"file_{i}"])
        if len(chapter_name) == 0:
            chapter_name = f"Глава {request.form['chapter_num']}"
        if not bd_connect.BDConnect.add_work_chapter(
                get_db(), request.form["id"], chapter_name, int(request.form["chapter_num"]), files):
            return {"status": "error", "code": 400, "message": "Just error"}
        return {"status": "success", "data": {}}

    @app.route("/api/resources/all_work_genres")
    def get_all_work_genres():
        return {"status": "success", "data": genre_template.Genre.get_work_dict_genre()}
