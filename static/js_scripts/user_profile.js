const user_data = {
    user_login: getCookie("user_login"),
    user_password: getCookie("user_password")
};
let USER_READ_LIST_SCROLL_PROGRESS = 0;
let USER_READ_LIST_COUNT_LOAD = 30;
let USER_COMMENT_LIST_SCROLL_PROGRESS = 0;
let USER_COMMENT_LIST_COUNT_LOAD = 30;

function setCookie(name, value, days) {
      var expires = "";
      if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
      }
      document.cookie = name + "=" + value + expires + "; path=/";
    }

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1, c.length);
        } if (c.indexOf(nameEQ) === 0) {
            return c.substring(nameEQ.length, c.length);
        }
    }
    return null;
}


fetch("/api/user/user_info", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
}).then(response => response.json()).then(data => {
    var username = document.getElementById("user_login");
    var username_menu = document.getElementById("profile_menu_username");
    if (data["result"]){
        username.text = data["user_name"];
        username_menu.innerHTML = data["user_name"];
        username.href = "/user/" + data["user_name"] + "/";
    }else{
        username.href = "/login";
    }
}).catch(error => {
    alert(error);
});

function addReadList(){
    fetch("/api/user/read_list/get", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                "user_login": user_data.user_login,
                "user_password": user_data.user_password,
                "limit": USER_READ_LIST_COUNT_LOAD,
                "offset": USER_READ_LIST_SCROLL_PROGRESS * USER_READ_LIST_COUNT_LOAD
            }
        )
    }).then(response => response.json()).then(data => {

        if (data["result"]){
            var manga_list = document.getElementById("user-read-list");
            for(var i = 0; i < data["size"]; i++){
                var manga_item = '<div class="user-read-manga"><div class="user-read-manga-div">';
                var image_url = "/api/get_file?file_id=" + data["read_manga_list"][i]["manga_title_image"];
                manga_item += '<img src="' + image_url + '" alt="haha">';
                manga_item += '<div class="user-read-manga-body">';
                manga_item += '<h5> ' + data["read_manga_list"][i]["rus_manga_name"] + ' </h5>';
                manga_item += '<p> ' + data["read_manga_list"][i]["manga_description"] + ' </p></div></div>';
                manga_item += '<div class="user-read-manga-buttons">';
                manga_item += '<button onclick="btn_manga_read_list_goto(' + "'" + data["read_manga_list"][i]["manga_name"];
                manga_item += "'" + ')" class="user-read-manga-button-read"> Читать  </button>';
                manga_item += '<button onclick="btn_manga_read_list_del(' + "'" + data["read_manga_list"][i]["manga_name"];
                manga_item += "')" + '" class="user-read-manga-button-del"> Убрать </button>';
                manga_item += '</div></div>';
                manga_list.innerHTML += manga_item;
            }
        }
    }).catch(error => {
        alert(error);
    });
}

function addCommentList(){
    fetch("/api/user/comment_list/get", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                "user_login": user_data.user_login,
                "user_password": user_data.user_password,
                "limit": USER_COMMENT_LIST_COUNT_LOAD,
                "offset": USER_COMMENT_LIST_SCROLL_PROGRESS * USER_COMMENT_LIST_COUNT_LOAD
            }
        )
    }).then(response => response.json()).then(data => {

        if (data["result"]){
            let manga_list = document.getElementById("user-comment-list");
            for(let i = 0; i < data["comments"].length; i++){
                let comment_item = '<div class="element-comment-list">';
                comment_item += '<div class="comment-title"><div class="comment-title-user">';
                comment_item += '<h5> ' + data["comments"][i]["rus_manga_name"] + ' </h5>';
                comment_item += '<h5> ' + user_data.user_login + ' </h5>';
                comment_item += '<p> [' + data["comments"][i]["manga_rating"] + '/10] </p>';
                comment_item += '</div><p class="comment-body"> ' + data["comments"][i]["comment"] + ' </p>';
                comment_item += '</div><div class="comment-btn">';
                comment_item += '<button onclick="btn_manga_read_list_goto(' + "'" + data["comments"][i]["manga_name"];
                comment_item += "'" + ')" class="user-read-manga-button-read"> К манге </button>';
                comment_item += '<button onclick="btn_user_comment_del(' + "'" + data["comments"][i]["manga_name"];
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


addReadList();
addCommentList();
// Смена страниц отображения при нажатии на кнопки из меню
let menuButtons = document.getElementsByClassName('menu-btn');
for (let i = 0; i < menuButtons.length; i++) {
    let page_admin_tools = document.getElementById('page-user-admin-tools');
    let page_user_read_list = document.getElementById('user-read-list');
    let page_user_comment_list = document.getElementById('user-comment-list');
    let page_setting = document.getElementById('page-setting');
    menuButtons[i].addEventListener('click', function() {
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
        } else if (target === 'setting'){
            page_setting.style.display = 'block';
        } else if(target === 'exit'){
            setCookie("user_login", "", 1);
            setCookie("user_password", "", 1);
            location.href = "";
        }
    });
}