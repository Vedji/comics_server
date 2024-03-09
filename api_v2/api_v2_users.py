import flask
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask import request, jsonify, Response
from datetime import timedelta
import basedata_helper
import api_v2.returning_values


# basedata_helper.BDHelper.get_db()
def init_api_v2_users(app: flask.app.Flask, get_db, jwt):

    @app.route('/api/v2/user', methods=["GET"])
    def api_v2_get_user_info():
        username = request.args.get("username", None, str)
        id_user = request.args.get("id_user", None, int)
        if username is None and id_user is None:
            return api_v2.returning_values.return_error("username or id_user will be filled", 400)
        user_info = None
        if username and basedata_helper.bd_user.BDUser.is_user_exists_by_his_username(get_db(), username):
            user_info = basedata_helper.bd_user.BDUser.get_user_info_for_his_username(get_db(), username)
        if id_user and basedata_helper.bd_user.BDUser.is_user_exists_by_his_id(get_db(), id_user):
            user_info = basedata_helper.bd_user.BDUser.get_user_info_for_his_id(get_db(), id_user)
        if user_info is not None:
            return api_v2.returning_values.return_success(user_info, 200)
        return api_v2.returning_values.return_error("User is not exists", 404)

    @app.route('/api/v2/user', methods=["POST"])
    def api_v2_user_authorization():
        if "username" not in request.json or "password" not in request.json:
            return api_v2.returning_values.return_error("username or id_user will be filled", 400)
        username = request.json["username"]
        password = request.json["password"]
        data = basedata_helper.bd_user.BDUser.check_user_authorization(get_db(), username, password)
        if data:
            access_token = create_access_token(identity=data["id_user"], additional_claims=data)
            return api_v2.returning_values.return_success({"access_token": access_token, **data}, 200)
        return api_v2.returning_values.return_error("Incorrect user data", 403)

    @app.route('/api/v2/user/registration', methods=["POST"])
    def api_v2_user_registration():
        if "username" not in request.json or "password" not in request.json:
            return api_v2.returning_values.return_error("username or id_user will be filled", 400)
        username = request.json["username"]
        password = request.json["password"]
        if basedata_helper.bd_user.BDUser.is_user_exists_by_his_username(get_db(), username):
            return api_v2.returning_values.return_error(f"User with username {username} already exists", 409)
        data = basedata_helper.bd_user.BDUser.user_registration(get_db(), username,  password)
        if data:
            access_token = create_access_token(identity=data["id_user"], additional_claims=data)
            return api_v2.returning_values.return_success({"access_token": access_token, **data}, 200)
        return api_v2.returning_values.return_error("Incorrect user data", 403)

