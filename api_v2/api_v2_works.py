import flask
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask import request, jsonify, Response
import basedata_helper
import api_v2.returning_values


def init_api_v2_works(app: flask.app.Flask, get_db, jwt):

    @app.route('/api/v2/works', methods=["GET"])
    def api_v2_works_catalog():
        limit = request.args.get("limit", -1, int)
        offset = request.args.get("offset", 0, int)
        _filter = request.args.get("filter", "", str)
        _sortby = request.args.get("sortby", "", str)

        if _filter == "fts":
            query = request.args.get("query", None, str)
            if query is None:
                return api_v2.returning_values.return_error("query argument is none", 400)
            return api_v2.returning_values.return_success(
                basedata_helper.bd_work.BDWork.ft_search_work(get_db(), query, limit, offset), 200)
        if _filter == "genre":
            query = request.args.get("query", None, int)
            if query is None:
                return api_v2.returning_values.return_error("genre argument is none", 400)
            return api_v2.returning_values.return_success(
                basedata_helper.bd_work.BDWork.get_by_genre(get_db(), query, limit, offset), 200)
        data = basedata_helper.bd_work.BDWork.get_all(get_db(), limit, offset)
        if data:
            return api_v2.returning_values.return_success(data, 200)
        return api_v2.returning_values.return_error("How? No works", 404)

    @app.route("/api/v2/works", methods=["POST"])
    @jwt_required()
    def api_v2_works_add():
        if "id_work" not in request.json:
            return api_v2.returning_values.return_error("No argument id_work", 400)
        if "id_user" not in request.json:
            return api_v2.returning_values.return_error("No argument id_user", 400)
        if "rus_name" not in request.json:
            return api_v2.returning_values.return_error("No argument rus_name", 400)
        if "eng_name" not in request.json:
            return api_v2.returning_values.return_error("No argument eng_name", 400)
        if "description" not in request.json:
            return api_v2.returning_values.return_error("No argument description", 400)
        if "genre" not in request.json:
            return api_v2.returning_values.return_error("No argument genre", 400)
        if not request.json["genre"].isdigit():
            return api_v2.returning_values.return_error("Argument genre is not a num", 400)
        if "pre_img" not in request.json:
            return api_v2.returning_values.return_error("No image file", 400)
        id_work = request.json["id_work"]
        id_user = request.json["id_user"]
        rus_name = request.json["rus_name"]
        eng_name = request.json["eng_name"]
        description = request.json["description"]
        genre = request.json["genre"]
        file = request.json["pre_img"]
