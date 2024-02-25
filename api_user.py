import flask
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask import request, jsonify
import bd_connect
from datetime import timedelta


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
        expires = timedelta(hours=1)
        access_token = create_access_token(identity=username, expires_delta=expires, additional_claims=data)
        return jsonify({"status": "success", "data": {"access_token": access_token}})

    @app.route('/api/v1/user/registration', methods=['POST'])
    @jwt_required()
    def _api_user_registration():
        print(get_jwt())
        current_user_id = get_jwt_identity()
        print(current_user_id)
        return jsonify(logged_in_as=current_user_id), 200

    @app.route('/api/v1/user/likes', methods=['GET'])
    @jwt_required()
    def api_get_user_likes():
        limit = request.args.get('limit', -1, int)
        offset = request.args.get('offset', 0, int)
        header_login = get_jwt()
        data = bd_connect.BDConnect.get_user_likes_catalog(get_db(), header_login["ID"], limit, offset)
        return jsonify({"status": "success", "data": {"likes_list": data}}), 200

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
            "data": {
                "user_comments_list": data,
                "user_id": header_login["ID"]
            }
        }
