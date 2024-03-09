import basedata_helper
import api_v2.api_v2_works
import api_v2.api_v2_users
import api_v2.returning_values
from flask import Flask, request, render_template, g
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import flask
import flask_jwt_extended


def init(app: flask.app.Flask, jwt: flask_jwt_extended.JWTManager):
    basedata_helper.bd_helper.BDHelper.init("SQLite", "basedata_helper/basedata_test.db")
    test_connection = basedata_helper.bd_helper.BDHelper.get_db
    api_v2.api_v2_users.init_api_v2_users(app, test_connection, jwt)  # Init api_v2 v2 for users
    api_v2.api_v2_works.init_api_v2_works(app, test_connection, jwt)  # Init api_v2 v2 for works
