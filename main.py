import bd_connect
import sqlite3
from flask import Flask, request, jsonify, render_template, send_file, g
import api_mobile, api_site
import API_DESCRIPTION


app = Flask(__name__)


def get_db():
    """ Возвращает объект соединения с БД"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(bd_connect.BDConnect.BD_NAME)
    return db


api_mobile.init_mobile_api(app, get_db)
api_site.init_site_api(app, get_db)


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
    manga_list = []
    manga_name_list = bd_connect.BDConnect.get_list_manga_name(get_db(), -1, 0)
    for i in manga_name_list["list_manga_name"]:
        buff = bd_connect.BDConnect.get_info_manga(get_db(), i)
        manga_list.append([buff["manga_name"], buff["manga_description"], buff["manga_title_image"]])
    return render_template("m_catalog/catalog_manga.html", title="Home", manga_list=manga_list)


@app.route('/catalog_manga/<manga_name>/')
def web_info_manga(manga_name: str):
    manga_info = bd_connect.BDConnect.get_info_manga(get_db(), manga_name)
    if not manga_info:
        return f"manga: {manga_name} is not exists", 404
    id_manga_title_image = manga_info["manga_title_image"]
    manga_description = manga_info["manga_description"]
    chapter_list = bd_connect.BDConnect.get_list_manga_chapters(get_db(), manga_name)
    chapter_list = [
        (
            item["chapter_number"],
            item["chapter_name"],
            item["chapter_len"]
        ) for item in chapter_list["list_manga_chapters"]]
    return render_template(
        "m_catalog/manga_view_info.html",
        title=manga_name,
        id_manga_title_image=id_manga_title_image,
        manga_name=manga_name,
        manga_description=manga_description,
        chapter_list=chapter_list
    )


@app.route('/catalog_manga/<manga_name>/read')
def web_read_manga(manga_name: str):
    chapter_number = request.args.get("c")
    chapter_number = int(chapter_number) if chapter_number and chapter_number.isdigit() else -1
    page_number = request.args.get("p")
    page_number = int(page_number) if page_number and page_number.isdigit() else -1
    if chapter_number < 0 or page_number < 0:
        return "Page Not Found /", 404
    data = bd_connect.BDConnect.get_info_chapter(get_db(), manga_name, chapter_number)
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
        map(lambda x: x[1], bd_connect.BDConnect.sql_command(get_db(), f"PRAGMA table_info('{table_name}');")))
    table_data = bd_connect.BDConnect.sql_command(get_db(), f"SELECT * FROM {table_name}")
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
        api_desc=API_DESCRIPTION.api_desc
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
