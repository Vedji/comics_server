import flask
from flask import request, jsonify, send_file
import api_v1.bd_connect


def init_mobile_api(app: flask.app.Flask, get_db):
    @app.route('/api/user/is_login', methods=['GET'])  # For mobile app
    def api_user_login():
        lgn = request.args.get("lgn")
        psw = request.args.get("psw")
        res = api_v1.bd_connect.BDConnect.get_user_login(get_db(), lgn, psw)
        return jsonify(res)

    @app.route('/api/user/comment_to_manga/add', methods=['POST'])  # For mobile app
    def api_user_add_comments():
        lgn = request.json["lgn"]
        psw = request.json["psw"]
        mid = request.json["mid"]
        com = request.json["com"]
        try:
            rating = request.json["rating"]
            rating = int(rating)
            return jsonify(api_v1.bd_connect.BDConnect.add_comments(get_db(), lgn, psw, mid, com, rating))
        except ValueError or TypeError:
            return jsonify({"user_authorization": True, "commit": False})

    @app.route('/api/get_list/manga_name', methods=['GET'])  # For mobile app
    def api_get_list_manga_name():
        limit = request.args.get("limit")
        offset = request.args.get("offset")
        rever = request.args.get("r")
        limit = int(limit) if limit and limit.isdigit() else -1
        offset = int(offset) if offset and offset.isdigit() else 0
        rever = True if rever and rever.isdigit() and rever == "1" else False
        return jsonify(api_v1.bd_connect.BDConnect.get_list_manga_name(get_db(), limit, offset, rever))

    @app.route('/api/user/comment_to_manga/get_list', methods=['GET'])  # For mobile app
    def api_user_get_comments():
        mid = request.args.get("mid")
        return jsonify(api_v1.bd_connect.BDConnect.get_comments_list(get_db(), mid))

    @app.route('/api/user/comment_to_manga/get', methods=['GET'])  # For mobile app
    def api_user_get_all_comment():
        lgn = request.args.get("lgn")
        mid = request.args.get("mid")
        return jsonify(api_v1.bd_connect.BDConnect.get_comment(get_db(), mid, lgn))

    @app.route('/api/user/comment_to_manga/is_added', methods=['GET'])  # For mobile app
    def api_is_user_add_comment_to_manga():
        lgn = request.args.get("lgn")
        mid = request.args.get("mid")
        return jsonify(api_v1.bd_connect.BDConnect.is_user_set_comment(get_db(), lgn, mid))

    @app.route('/api/user/comment_to_manga/del', methods=['POST'])  # For mobile app
    def api_user_del_comments():
        lgn = request.json["lgn"]
        psw = request.json["psw"]
        mid = request.json["mid"]
        return jsonify(api_v1.bd_connect.BDConnect.delete_user_comment(get_db(), lgn, psw, mid))

    @app.route('/api/user/likes_list/get', methods=['GET'])  # For mobile app
    def api_user_likes_list_get():
        lgn = request.args.get("lgn")
        psw = request.args.get("psw")
        return jsonify(api_v1.bd_connect.BDConnect.get_like_manga_user(get_db(), lgn, psw))

    @app.route('/api/user/likes_list/add_manga', methods=['GET'])  # For mobile app
    def api_user_likes_list_add_manga():
        lgn = request.args.get("lgn")
        psw = request.args.get("psw")
        manga_name = request.args.get("mid")
        return jsonify(api_v1.bd_connect.BDConnect.add_manga_in_like_manga_user(get_db(), lgn, psw, manga_name))

    @app.route('/api/user/likes_list/manga_in', methods=['GET'])  # For mobile app
    def api_user_likes_list_manga_in():
        lgn = request.args.get("lgn")
        psw = request.args.get("psw")
        manga_name = request.args.get("mid")
        return jsonify(api_v1.bd_connect.BDConnect.manga_in_likes_list(get_db(), lgn, psw, manga_name))

    @app.route('/api/user/comments/get', methods=['GET'])  # For mobile app
    def api_user_get_all_comments_user():
        lgn = request.args.get("lgn")
        psw = request.args.get("psw")
        res = api_v1.bd_connect.BDConnect.get_user_comments_list(get_db(), lgn, psw)
        return jsonify(res)

    @app.route('/api/user/registration', methods=['GET'])  # For mobile app
    def api_user_registration():
        lgn = request.args.get("lgn")
        psw = request.args.get("psw")
        return jsonify({"is_registration_ok": api_v1.bd_connect.BDConnect.user_registration(get_db(), lgn, psw)})

    @app.route('/api/get_status/server')  # For mobile app
    def api_get_server_status():
        server_status = {
            "server_status": True
        }
        return jsonify(server_status)

    @app.route('/api/get_info/manga', methods=['GET'])  # For mobile app
    def api_get_info_manga():
        manga_name = request.args.get("n")
        return jsonify(api_v1.bd_connect.BDConnect.get_info_manga(get_db(), manga_name))

    @app.route('/api/get_file', methods=['GET'])  # For mobile app
    def api_get_file():
        file_id = request.args.get("file_id")
        file_id = int(file_id) if file_id and file_id.isdigit() else -1
        return send_file(
            api_v1.bd_connect.BDConnect.get_file(get_db(), file_id),
            download_name=api_v1.bd_connect.BDConnect.get_info_file(get_db(), file_id)['image_name'])

    @app.route('/api/get_list/manga_chapters', methods=['GET'])  # For mobile app
    def api_get_list_manga_chapters():
        manga_name = request.args.get("manga_name")
        return jsonify(api_v1.bd_connect.BDConnect.get_list_manga_chapters(get_db(), manga_name))

    @app.route('/api/get_info/page', methods=['GET'])  # For mobile app
    def api_get_info_page():
        manga_name = request.args.get("manga_name")
        chapter_number = request.args.get("chapter_number")
        chapter_number = int(chapter_number) if chapter_number and chapter_number.isdigit() else -1
        page_number = request.args.get("page_number")
        page_number = int(page_number) if page_number and page_number.isdigit() else -1
        return jsonify(api_v1.bd_connect.BDConnect.get_info_page(get_db(), manga_name, chapter_number, page_number))

    @app.route('/api/get_info/chapter', methods=['GET'])
    def api_get_info_chapter():
        manga_name = request.args.get("manga_name")
        chapter_number = request.args.get("chapter_number")
        chapter_number = int(chapter_number) if chapter_number and chapter_number.isdigit() else -1
        return jsonify(api_v1.bd_connect.BDConnect.get_info_chapter(get_db(), manga_name, chapter_number))

    @app.route('/api/get_info/file', methods=['GET'])
    def api_get_info_file():
        file_id = request.args.get("file_id")
        file_id = int(file_id) if file_id and file_id.isdigit() else -1
        return jsonify(api_v1.bd_connect.BDConnect.get_info_file(get_db(), file_id))

    @app.route('/api/get_len/chapter', methods=['GET'])
    def api_get_len_chapter():
        manga_name = request.args.get("manga_name")
        chapter_number = request.args.get("chapter_number")
        chapter_number = int(chapter_number) if chapter_number and chapter_number.isdigit() else -1
        return jsonify({"len": api_v1.bd_connect.BDConnect.get_len_chapter(get_db(), manga_name, chapter_number)})
