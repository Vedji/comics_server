let USER_READ_LIST_SCROLL_PROGRESS = 0;
let USER_READ_LIST_COUNT_LOAD = 30;
let USER_COMMENT_LIST_SCROLL_PROGRESS = 0;
let USER_COMMENT_LIST_COUNT_LOAD = 30;

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function load_page() {
    fetch("/api/v1/user", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        }
    }).then(response => response.json()).then(data => {
        let profile_menu_username = document.getElementById("profile_menu_username");
        if (data["status"] === "success") {
            let btn_admin_tools = document.getElementById("li-profile_menu_admin_tools");
            let list_admin_tools = document.getElementById("tools-admin-list");
            btn_admin_tools.style.display = "none";
            list_admin_tools.style.display = 'none';
            if (data["data"]["ROLE"] > 0 && data["data"]["ROLE"] < 3) {
                console.log("")
                btn_admin_tools.style.display = 'block';
                list_admin_tools.style.display = 'block';
            }
            profile_menu_username.textContent = data["data"]["USERNAME"];
        }
    }).catch(error => {
        alert(error);
    });
    // Смена страниц отображения при нажатии на кнопки из меню
    let menuButtons = document.getElementsByClassName('menu-btn');
    for (let i = 0; i < menuButtons.length; i++) {
        let page_admin_tools = document.getElementById('page-user-admin-tools');
        let page_user_read_list = document.getElementById('user-like-list');
        let page_user_comment_list = document.getElementById('user-comment-list');
        let page_setting = document.getElementById('page-setting');
        menuButtons[i].addEventListener('click', function () {
            let target = this.getAttribute('data-target');
            page_admin_tools.style.display = 'none';
            page_user_read_list.style.display = 'none';
            page_user_comment_list.style.display = 'none';
            page_setting.style.display = 'none';
            if (target === 'admin_tools') {
                page_admin_tools.style.display = 'block';
            } else if (target === 'read_list') {
                page_user_read_list.style.display = 'block';
            } else if (target === 'my_comments') {
                page_user_comment_list.style.display = 'block';
            } else if (target === 'setting') {
                page_setting.style.display = 'block';
            } else if (target === 'exit') {
                setCookie("access_token", "", 1);
                location.href = "";
            }
        });
    }
}

function addReadList(limit = -1, offset = 0){
    let params = {
        limit: limit,
        offset: offset
    }
    let paramToURL = new URLSearchParams(params).toString();
    let url = `/api/v1/user/likes?${paramToURL}`;
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        },
    }).then(response => response.json()).then(data => {
        if (data["status"] === "success"){
            let user_like_list_container = document.getElementById("user-like-list");
            for(let i = 0; i < data["data"]["likes_list"].length; i++){
                let image_url = "/api/get_file?file_id=" + data["data"]["likes_list"][i]["pre_img"];

                let user_read_manga = document.createElement("div");
                user_read_manga.setAttribute("class", "user-like-manga");

                let user_read_manga_desc = document.createElement("div");
                user_read_manga_desc.setAttribute("class", "user-read-manga-div");
                let img = document.createElement("img");
                img.setAttribute("src", image_url)
                img.setAttribute("alt", data["data"]["likes_list"][i]["ru_name"].toString());
                let user_like_manga_body = document.createElement("div");
                user_like_manga_body.setAttribute("class", "user-read-manga-body");
                let h5 = document.createElement("h5");
                h5.textContent = data["data"]["likes_list"][i]["ru_name"].toString();
                let desc_p = document.createElement("p");
                desc_p.textContent = data["data"]["likes_list"][i]["desc"].toString();
                user_like_manga_body.appendChild(h5);
                user_like_manga_body.appendChild(desc_p);
                user_read_manga_desc.appendChild(user_like_manga_body);
                user_read_manga.appendChild(user_read_manga_desc);

                let user_read_manga_buttons = document.createElement("div");
                user_read_manga_buttons.setAttribute("class", "user-read-manga-buttons");
                let btn_1 = document.createElement("a");
                btn_1.setAttribute("class", "user-read-manga-button-read");
                btn_1.setAttribute(
                    "href", `/catalog_manga/${data["data"]["likes_list"][i]["work_id"]}`)
                btn_1.textContent = "Читать";
                let btn_2 = document.createElement("a");
                btn_2.setAttribute("class", "user-read-manga-button-del");
                btn_2.textContent = "Удалить";
                user_read_manga_buttons.appendChild(btn_1);
                user_read_manga_buttons.appendChild(btn_2);
                user_read_manga_desc.appendChild(user_read_manga_buttons);
                user_like_list_container.appendChild(user_read_manga);
            }
        }
    }).catch(error => {
        alert(error);
    });
}

function addCommentList(limit = -1, offset = 0){
    let params = {
        limit: limit,
        offset: offset
    }
    let paramToURL = new URLSearchParams(params).toString();
    let url = `/api/v1/user/comments?${paramToURL}`;
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        },
    }).then(response => response.json()).then(data => {
        if (data["status"] === "success"){
            let manga_list = document.getElementById("user-comment-list");
            for(let i = 0; i < data["data"]["user_comments_list"].length; i++){
                let _ru_name = data["data"]["user_comments_list"][i]["ru_name"];
                let _work_id = data["data"]["user_comments_list"][i]["work_id"];
                let _grade = data["data"]["user_comments_list"][i]["grade"];
                let _comment = data["data"]["user_comments_list"][i]["comment"];

                let comment_item = '<div class="element-comment-list">';
                comment_item += '<div class="comment-title"><div class="comment-title-user">';
                comment_item += '<h5> ' + _ru_name + ' </h5>';
                comment_item += '<p> [' + _grade + '/10] </p>';
                comment_item += '</div><p class="comment-body"> ' + _comment + ' </p>';
                comment_item += '</div><div class="comment-btn">';
                comment_item += '<button onclick="btn_manga_read_list_goto(' + "'" + _work_id;
                comment_item += "'" + ')" class="user-read-manga-button-read"> К манге </button>';
                comment_item += '<button onclick="btn_user_comment_del(' + "'" + _work_id;
                comment_item += "')"+ '" class="user-read-manga-button-del"> Удалить </button>';
                comment_item += '</div></div></div>';
                manga_list.innerHTML += comment_item;
            }
        }
    }).catch(error => {
        alert(error);
    });
}

function btn_manga_read_list_goto(manga_name){
    location.href = "/catalog_manga/" + manga_name + "/";
}

function btn_manga_read_list_del(manga_name){
    fetch("/api/catalog/manga/set_read", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(
        {
            "user_login": user_data.user_login,
            "user_password": user_data.user_password,
            "manga_name": manga_name
        }
    )}).then(response => response.json()).then(data => {
        if (data["result"]){
            location.href = "/user/" + data.user_login + "/"
        }
    }).catch(error => {
        alert(error);
    });
}

function btn_user_comment_del(manga_name){
    fetch("/api/user/del_comment", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(
        {
            "user_login": user_data.user_login,
            "user_password": user_data.user_password,
            "manga_name": manga_name
        }
    )}).then(response => response.json()).then(data => {
        if (data["result"]){
            location.href = "/user/" + data.user_login + "/"
        }
    }).catch(error => {
        alert(error);
    });
}

load_page();
addReadList();
addCommentList();


