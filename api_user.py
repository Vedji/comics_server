import flask
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask import request, jsonify
import bd_connect
from datetime import timedelta
import exception


def init_site_api(app: flask.app.Flask, get_db, jwt):

    @app.route('/api/v1/user', methods=["GET"])
    @jwt_required()
    def api_get_user_info():
        user_id = get_jwt()["ID"]
        return jsonify({"status": "success", "data": bd_connect.BDConnect.is_user_exists(get_db(), user_id)})

    @app.route('/api/v1/user/login', methods=['POST'])
    def _api_user_login():
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        data = bd_connect.BDConnect.get_user_info(get_db(), username, password)
        if not data:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401
        expires = timedelta(days=1)
        access_token = create_access_token(identity=username, expires_delta=expires, additional_claims=data)
        return jsonify({"status": "success", "data": {
            "access_token": access_token, "ID": data["ID"], "USER_ROLE": data["ROLE"], "USERNAME": data["USERNAME"]}})

    @app.route('/api/v1/user/registration', methods=['POST'])
    def _api_user_registration():
        if "username" not in request.json or "password" not in request.json:
            return jsonify({"status": "error", "code": 400, "message": "No password or username"}), 400
        username = request.json["username"]
        password = request.json["password"]
        if bd_connect.BDConnect.is_user(get_db(), username):
            return jsonify({"status": "error", "code": 400, "message": "User has exists"}), 400
        data = bd_connect.BDConnect.user_reg(get_db(), username, password)
        expires = timedelta(days=1)
        access_token = create_access_token(identity=data["USERNAME"], expires_delta=expires, additional_claims=data)
        return jsonify({
            "status": "success",
            "code": 201,
            "message": "User Created",
            "data": {
                "access_token": access_token,
                "ID": data["ID"],
                "USER_ROLE": data["USER_ROLE"],
                "USERNAME": data["USERNAME"]
            }
        }), 201

    @app.route('/api/v1/user/likes', methods=['GET'])
    @jwt_required()
    def api_get_user_likes():
        limit = request.args.get('limit', -1, int)
        offset = request.args.get('offset', 0, int)
        header_login = get_jwt()
        data = bd_connect.BDConnect.get_user_likes_catalog(get_db(), header_login["ID"], limit, offset)
        return jsonify({"status": "success", "data": data}), 200

    @app.route('/api/v1/user/likes/<work_id>', methods=["GET"])
    @jwt_required()
    def api_get_user_like_work(work_id: str):
        header_login = get_jwt()
        data = bd_connect.BDConnect.is_user_like_work(get_db(), header_login["ID"], work_id)
        if data is None:
            return jsonify({"status": "error", "code": 404, "message": "Work is not exists"}), 404
        return jsonify({"status": "success", "data": {"user_like": data}}), 200

    @app.route('/api/v1/user/likes/<work_id>', methods=["POST"])
    @jwt_required()
    def api_set_user_like_work(work_id: str):
        header_login = get_jwt()
        data = bd_connect.BDConnect.set_user_like_work(get_db(), header_login["ID"], work_id)
        if data is None:
            return jsonify({"status": "error", "code": 404, "message": "Work is not exists"}), 404
        return jsonify({"status": "success", "data": {"user_like": data}}), 200

    @app.route('/api/v1/user/comments', methods=["GET"])
    @jwt_required()
    def api_get_user_comments_list():
        limit = request.args.get('limit', -1, int)
        offset = request.args.get('offset', 0, int)
        header_login = get_jwt()
        data = bd_connect.BDConnect.get_user_comment_list(get_db(), header_login["ID"], limit, offset)
        return {
            "status": "success",
            "data": data
        }

    @app.route('/api/v1/user/comments/<work_id>', methods=["GET"])
    @jwt_required()
    def api_get_user_works_comment(work_id: str):
        header_login = get_jwt()
        try:
            data = bd_connect.BDConnect.get_user_comment(get_db(), header_login["ID"], work_id)
            return jsonify({
                "status": "success",
                "data": data
            }), 200
        except exception.NotExists as body:
            return jsonify({"status": "error", "message": body.__str__()}), 404

    @app.route('/api/v1/user/comments/<work_id>', methods=["DELETE"])
    @jwt_required()
    def api_del_user_works_comment(work_id: str):
        user_data = get_jwt()
        per = user_data["ROLE"]
        comm_id = request.args.get("user_id", user_data["ID"], int)
        if user_data["ID"] != comm_id and (per > 2 or per < 1):
            return jsonify({"status": "error", "code": 401, "message": "No Permission"}), 401
        bd_connect.BDConnect.del_works_comment(get_db(), user_data["ID"], work_id)
        return jsonify({"status": "success", "data": {}}), 200

    @app.route('/api/v1/user/comments/<work_id>', methods=["POST"])
    @jwt_required()
    def api_add_user_works_comment(work_id: str):
        user_data = get_jwt()
        rating, msg, _ = exception.get_arg(request.json["rating"], lambda x: int(x), "rating")
        if msg["status"] == "error":
            return jsonify(msg), msg["code"]
        comment, msg, _ = exception.get_arg(request.json["comment"], lambda x: str(x), "comment")
        if msg["status"] == "error":
            return jsonify(msg), msg["code"]
        data, msg, _ = exception.req_fun(
            lambda: bd_connect.BDConnect.append_works_comment(get_db(), user_data["ID"], work_id, rating, comment))
        if msg["status"] == "error":
            return jsonify(msg), msg["code"]
        return jsonify({"status": "success", "data": {}}), 200

    @app.route('/api/v1/user/comments/<work_id>', methods=["PUT"])
    @jwt_required()
    def api_upd_user_works_comment(work_id: str):
        user_data = get_jwt()
        rating, msg, _ = exception.get_arg(request.json["rating"], lambda x: int(x), "rating")
        if msg["status"] == "error":
            return jsonify(msg), msg["code"]
        comment, msg, _ = exception.get_arg(request.json["comment"], lambda x: str(x), "comment")
        if msg["status"] == "error":
            return jsonify(msg), msg["code"]
        data, msg, _ = exception.req_fun(
            lambda: bd_connect.BDConnect.update_works_comment(get_db(), user_data["ID"], work_id, rating, comment))
        if msg["status"] == "error":
            return jsonify(msg), msg["code"]
        return jsonify({"status": "success", "data": {}}), 200
