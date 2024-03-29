import sqlite3
import flask
import flask_jwt_extended
from flask import request, render_template, g
import api_v1.API_DESCRIPTION
import api_v1.api_mobile
import api_v1.api_resources
import api_v1.api_user
import api_v1.api_site
import api_v1.api_work
import api_v1.bd_connect


def init(app: flask.app.Flask, jwt: flask_jwt_extended.JWTManager):
    def get_db():
        """ Возвращает объект соединения с БД"""
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(api_v1.bd_connect.BDConnect.BD_NAME)
        return db

    api_v1.api_mobile.init_mobile_api(app, get_db)
    api_v1.api_site.init_site_api(app, get_db)
    # api_works.init_site_api(app, get_db)          # init works api_v2 (lattest)
    api_v1.api_resources.init_site_api(app, get_db)        # init resources api_v2
    api_v1.api_work.init_site_api(app, get_db)             # init work api_v2
    api_v1.api_user.init_site_api(app, get_db, jwt)        # init user api_v2

    @app.route('/login')
    def web_user_login():
        return render_template("user_login.html")

    @app.route('/registration')
    def web_user_registration():
        return render_template("user_registration.html")

    @app.route('/user/<user_name>/')
    def web_user_profile(user_name):
        return render_template("user_profile.html")

    @app.route('/')
    @app.route('/index')
    @app.route('/catalog_manga')
    def web_catalog_manga():
        if "Mobile" in request.headers.get('User-Agent'):
            return render_template("mobile/catalog/m_catalog.html")
        return render_template("m_catalog/catalog_manga.html")

    @app.route('/catalog_manga/<manga_name>/')
    def web_info_manga(manga_name: str):
        manga_info = api_v1.bd_connect.BDConnect.get_info_manga(get_db(), manga_name)
        if not manga_info:
            return f"manga: {manga_name} is not exists", 404
        if "Mobile" in request.headers.get('User-Agent'):
            return render_template("mobile/work_view/m_section_info.html")
        return render_template("m_catalog/manga_view_info.html")

    @app.route('/catalog_manga/<manga_name>/read')
    def web_read_manga(manga_name: str):
        chapter_number = request.args.get("c")
        chapter_number = int(chapter_number) if chapter_number and chapter_number.isdigit() else -1
        page_number = request.args.get("p")
        page_number = int(page_number) if page_number and page_number.isdigit() else -1
        if chapter_number < 0 or page_number < 0:
            return "Page Not Found /", 404
        data = api_v1.bd_connect.BDConnect.get_info_chapter(get_db(), manga_name, chapter_number)
        if not data or data["chapter_len"] < page_number:
            return "Page Not Found /", 404
        return render_template("m_catalog/manga_read.html")

    @app.route('/all_bd_view')
    def web_all_bd_view():
        bd_names = [
            "manga",
            "chapters",
            "pages",
            "files",
            "user_likes_catalog",
            "comments",
            "users"
        ]
        return render_template("bd_view/all_bd_view.html", bd_names=bd_names)

    @app.route('/bd_view/<table_name>/')
    def web_bd_view(table_name):
        heads = tuple(
            map(lambda x: x[1], api_v1.bd_connect.BDConnect.sql_command(
                get_db(), f"PRAGMA table_info('{table_name}');")))
        table_data = api_v1.bd_connect.BDConnect.sql_command(get_db(), f"SELECT * FROM {table_name}")
        return render_template(
            "bd_view/bd_view.html",
            bd_name=table_name,
            bd_heads=heads,
            table_data=table_data
        )

    @app.route('/api_documentation')
    def web_api_documentation():
        return render_template(
            "api_documentation.html",
            api_desc=api_v1.API_DESCRIPTION.api_desc
        )

    @app.route('/editor_add_manga')
    def web_add_manga():
        return render_template("editor/editor_add_manga.html")

    @app.route('/editor_add_chapter')
    def web_add_chapter():
        return render_template("editor/editor_add_chapter.html")
