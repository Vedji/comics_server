import flask
from flask import request
from api_v1 import bd_connect
from api_v1.genre_template import Genre

def init_site_api(app: flask.app.Flask, get_db):
    @app.route('/api/works/catalog', methods=["GET"])
    def api_works_catalog():
        limit = -1
        offset = 0
        template = Genre.get_null_genre()

        if request.args.get("limt"):
            if not request.args.get("limt").isdigit():
                return {"status": "error", "code": 400, "message": "Argument limt is not a number"}
            limit = int(request.args.get("limt"))
        if request.args.get("offs"):
            if not request.args.get("offs").isdigit():
                return {"status": "error", "code": 400, "message": "Argument offs is not a number"}
            offset = int(request.args.get("offs"))
        if request.args.get("temp"):
            if not Genre.check_temp(request.args.get("temp")):
                return {"status": "error", "code": 400, "message": "Argument temp is not a correct"}
            template = request.args.get("temp")
        data = bd_connect.BDConnect.get_works_catalog(get_db(), limit, offset, template)
        return {
            "status": "success",
            "data": data
        }

    @app.route('/api/works/search', methods=["GET"])
    def api_works_search():
        limit = -1
        offset = 0
        template = request.args.get("temp")

        if request.args.get("limt"):
            if not request.args.get("limt").isdigit():
                return {"status": "error", "code": 400, "message": "Argument limt is not a number"}
            limit = int(request.args.get("limt"))
        if request.args.get("offs"):
            if not request.args.get("offs").isdigit():
                return {"status": "error", "code": 400, "message": "Argument offs is not a number"}
            offset = int(request.args.get("offs"))
        if not template:
            return {"status": "error", "code": 400, "message": "Argument temp is not a exists"}
        template = template.replace("+", " ", -1)
        data = bd_connect.BDConnect.get_catalog_search(get_db(), limit, offset, template)
        print(template)
        print(data)
        return {
            "status": "success",
            "data": data
        }



