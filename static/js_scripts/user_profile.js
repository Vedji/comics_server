let urlParameters = new URLSearchParams(window.location.search);
let page_current = 0;
let page_count = 1;
let comments_list_length = 0;
let likes_list_length = 0;
let last_section = "None";
let user_role = 0;
let access_token = "";
let username = "Not AUTHORIZATION";
try { user_role = USER_ROLE; }catch (error){ console.log("USER_ROLE's not initialization"); }
try { access_token = ACCESS_TOKEN; }catch (error){ console.log("user not initialization, not ACCESS_TOKEN"); }
try { username = USERNAME; }catch (error){ console.log("user not authorization, not AUTHORIZATION"); }
// const
let page_load_limit = 2;

let sections = {
        "likes": {
            "permission": 0,
            "elements": [document.getElementById("page-user-likes-list")]
        },
        "comments": {
            "permission": 0,
            "elements": [document.getElementById("page-user-comments-list")]
        },
        "tools": {
            "permission": 2,
            "elements": [
                document.getElementById("page-tools"),
                document.getElementById("page-tools-add-new-work")
            ]
        },
        "exit": {
            "permission": 0,
            "elements": []
        }
    };

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}
function menu_button(target, per= 0, reload = false){
    if (reload || target !== last_section){
        page_current = 0;
        page_count = 1;
        if (urlParameters.has("_p") && last_section !== target)
            urlParameters.delete("_p");
    }
    last_section = target;
    document.getElementById("sidebar-username").textContent = username;

    for (let item in sections){
        if (!sections.hasOwnProperty(item))
            continue;
        if (item === target && per >= sections[item]["permission"]) {
            for (let i = 0; i < sections[item]["elements"].length; i++){
                sections[item]["elements"][i].style.display = 'block';
                sections[item]["elements"][i].style.background = '#2A4480';
            }
            continue;
        }
        for (let i = 0; i < sections[item]["elements"].length; i++) {
            sections[item]["elements"][i].style.background = '#303E60';
            sections[item]["elements"][i].style.display = 'none';
        }
    }
    if (target === "comments"){
        get_user_comment(page_load_limit, page_load_limit * page_current);
        urlParameters.set("_section", target);
        history.replaceState(null, null, "?" + urlParameters.toString());
        return;
    }
    if (target === "likes") {
        get_user_likes(page_load_limit, page_load_limit * page_current);
        urlParameters.set("_section", target);
        history.replaceState(null, null, "?" + urlParameters.toString());
        return;
    }
    if (target === "tools"){
        set_genres_to_tools_page();
        urlParameters.set("_section", target);
        history.replaceState(null, null, "?" + urlParameters.toString());
        return;
    }
    if (target === "exit"){
        setCookie("access_token", "", 1);
        setCookie("user_id", "", 1);
        setCookie("username", "", 1);
        setCookie("user_role", "", 1);
        location.href = "/"
        return;
    }
    urlParameters.delete("_section");
    urlParameters.delete("_p");
    history.replaceState(null, null, "?" + urlParameters.toString());
    location.href = "/login"
}
function get_user_likes(limit = -1, offset = 0) {
    let likes_list_container = document.getElementById("user-likes-list-items");
    likes_list_container.innerHTML = "";
    let params = {
        limit: limit,
        offset: offset
    }
    fetch(`/api/v1/user/likes?${(new URLSearchParams(params)).toString()}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        },
    }).then(response => response.json()).then(data => {
        if (data["status"] === "success"){
            page_count = data["data"]["pages_count"];
            likes_list_length = data["data"]["likes_list"].length;
            // let view_pages = document.getElementById("page-comment-view");
            // view_pages.textContent = `Страница [${comment_page_current+1}/${comment_page_count}]`
            for (let i = 0; i < data["data"]["likes_list"].length; i++){
                // container values
                let pre_img = data["data"]["likes_list"][i]["pre_img"];
                let work_name = data["data"]["likes_list"][i]["ru_name"];
                let work_id = data["data"]["likes_list"][i]["work_id"];
                let work_url = `/catalog_manga/${work_id}`;
                let img_url = `/api/get_file?file_id=${pre_img}`;
                // create element
                // header
                let header = document.createElement("div");
                header.setAttribute("class", "work-like-list-header");
                likes_list_container.appendChild(header);
                // body
                let body = document.createElement("div");
                body.setAttribute("class", "work-like-list-body");
                let img = document.createElement("img");
                img.setAttribute("src", img_url);
                img.setAttribute("alt", `Image not download ${work_id}`);
                body.appendChild(img);
                let name_container = document.createElement("div");
                name_container.setAttribute("class", "work-like-list-body-desc-name")
                let h3 = document.createElement("h3");
                let a = document.createElement("a");
                a.setAttribute("href", work_url);
                a.textContent = work_name;
                h3.appendChild(a);
                name_container.appendChild(h3);
                let p = document.createElement("p");
                p.textContent = `ID: ${work_id}`;
                name_container.appendChild(p);
                body.appendChild(name_container);
                // Button remove work
                let btn_remove = document.createElement("button");
                btn_remove.setAttribute("class", "btn_construct");
                btn_remove.textContent = "Убрать";
                btn_remove.onclick = () => { remove_like_work(work_id) };
                body.appendChild(btn_remove);
                likes_list_container.appendChild(body);
                let page_show = document.getElementById("page-likes-view");
                page_show.textContent = `Страница [${page_current+1}/${page_count}]`
            }
        }
    }).catch(error => {
        alert(error);
    });
}
// comments
function btn_delete_comment(work_id){
    fetch(`/api/v1/user/comments/${work_id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${access_token}`
        }
    }).then(response => {
        console.log("btn_delete_comment, code: ", response.status)
        return response.json()
    }).then(data => {
        if (data["status"] === "success") {
            if (comments_list_length - 1 === 0 && page_current !== 0)
                page_current -= 1;
            urlParameters.set("_section", "comments");
            urlParameters.set("_p", page_current.toString());
            history.replaceState(null, null, "?" + urlParameters.toString());
            location.reload();
        }
    }).catch(error => console.error(error));
}
function remove_like_work(work_id){
    fetch(`/api/v1/user/likes/${work_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
            body: JSON.stringify({})
        }).then(response => {
            return response.json()})
        .then(data => {
            if (data["status"] === "success"){
                if (likes_list_length - 1 === 0 && page_current !== 0)
                    page_current -= 1;
                urlParameters.set("_section", "likes");
                urlParameters.set("_p", page_current.toString());
                history.replaceState(null, null, "?" + urlParameters.toString());
                location.reload();
            }
        }).catch(error => {
            alert(error);
        });
}
function get_user_comment(limit = -1, offset = 0) {
    let comment_list_container = document.getElementById("comment-list-container");
    comment_list_container.innerHTML = "";
    let params = {
        limit: limit,
        offset: offset
    }
    fetch(`/api/v1/user/comments?${(new URLSearchParams(params)).toString()}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        },
    }).then(response => response.json()).then(data => {
        if (data["status"] === "success"){
            page_count = data["data"]["pages_count"];
            comments_list_length = data["data"]["user_comments_list"].length;
            let view_pages = document.getElementById("page-comment-view");
            view_pages.textContent = `Страница [${page_current+1}/${page_count}]`
            for (let i = 0; i < data["data"]["user_comments_list"].length; i++){
                // container values
                let comment = data["data"]["user_comments_list"][i]["comment"];
                let grade = data["data"]["user_comments_list"][i]["grade"];
                let work_name = data["data"]["user_comments_list"][i]["ru_name"];
                let work_id = data["data"]["user_comments_list"][i]["work_id"];
                let work_url = `/catalog_manga/${work_id}`;
                // create element
                // header
                let header = document.createElement("div");
                header.setAttribute("class", "comment-item-header");
                let h3 = document.createElement("h3");
                let title_name = document.createElement("a");
                title_name.setAttribute("href", work_url);
                title_name.textContent = work_name.toString();
                h3.appendChild(title_name);
                header.appendChild(h3);
                comment_list_container.appendChild(header);
                // body
                let body = document.createElement("div");
                body.setAttribute("class", "comment-item-body");
                let comment_text = document.createElement("p");
                comment_text.textContent = comment;
                body.appendChild(comment_text);
                comment_list_container.appendChild(body);
                // footer
                let footer = document.createElement("div");
                footer.setAttribute("class", "comment-item-footer");
                let btn_del_commit = document.createElement("button");
                btn_del_commit.setAttribute("class", "btn_construct");
                btn_del_commit.onclick = () => {btn_delete_comment(work_id)};
                btn_del_commit.textContent = "Delete";
                footer.appendChild(btn_del_commit);
                comment_list_container.appendChild(footer);
            }
        }
    }).catch(error => {
        alert(error);
    });
}

function set_genres_to_tools_page(){
    fetch("/api/resources/all_work_genres").then(function(response) {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    }).then(function(data) {
        if (data["status"] === "success") {
            let container = document.getElementById("page-tools-add-new-work-genres")
            container.innerHTML = "";
            for (let item in data["data"]) {
                console.log(data["data"][item]);
                let lbl = document.createElement("label");
                lbl.setAttribute("class", "checkbox-input");
                let inp = document.createElement("input");
                inp.setAttribute("type", "checkbox");
                inp.setAttribute("data-genre", data["data"][item]);
                inp.setAttribute("data-genre-index", item);
                inp.setAttribute("class", "tools-add-work-inp-genre")
                inp.checked = false;
                inp.hidden = true;
                lbl.appendChild(inp);
                let sps = document.createElement("span");
                sps.setAttribute("class", "checkbox-input-button");
                sps.textContent = data["data"][item];
                lbl.appendChild(sps);
                container.appendChild(lbl);
            }
        }
    }).catch(function(error) {
        console.log("There was a problem with the fetch operation: ", error.message);
    });
}
// load_page();
// addReadList();
// addCommentList();
document.getElementById("page-tools-add-new-work-file").addEventListener("input", function () {
    let msg = document.getElementById("page-tools-add-new-work-msg");
    if (!this.files[0]){
         msg.textContent = "А как?";
         return;
      }
    let reader = new FileReader();
    let img = document.getElementById("page-tools-add-new-work-img");
    reader.onload = function (r) {
        img.style.display = "block";
        img.src =  r.target.result;
    }
    reader.readAsDataURL(this.files[0]);
});

document.getElementById("page-tools-add-new-work-form")
    .addEventListener("submit", function(event) {
        event.preventDefault();
        let msg = document.getElementById("page-tools-add-new-work-msg");
        let formData = new FormData();
        let set_work_id = document.getElementById('page-tools-add-new-work-work-id');
        formData.append('work_id', set_work_id.value);
        let set_work_name = document.getElementById('page-tools-add-new-work-ru_name');
        formData.append('ru_name', set_work_name.value);
        let set_work_desc = document.getElementById('page-tools-add-new-work-desc');
        formData.append('desc', set_work_desc.value);
        let genres = document.querySelectorAll(".tools-add-work-inp-genre");
        let line_genre = Array(genres.length).fill("0");
        for (let i = 0; i < genres.length; i++){
            if (genres.item(i).hasAttribute("data-genre-index")){
                if (genres.item(i).checked)
                    line_genre[Number(genres.item(i).getAttribute("data-genre-index"))] = "1";
                else
                    line_genre[Number(genres.item(i).getAttribute("data-genre-index"))] = "0";
            }
        }
        line_genre = line_genre.join("");
        formData.append('genre', line_genre);
        let fileInput = document.getElementById('page-tools-add-new-work-file');
        if (!fileInput.files[0]){
               msg.textContent = "Загрузите изображение";
               return;
        }
        formData.append('pre_img', fileInput.files[0]);
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/v1/work', true);
        xhr.setRequestHeader("Authorization", `Bearer ${access_token}`);
        xhr.onload = function () {
            console.log(xhr);
            if (xhr.status === 200) {
                msg.textContent = "Глава успешно загруженна";
                msg.style.color = "green";
            }
            else if (xhr.status === 400 || xhr.status === 401){
                msg.textContent = JSON.parse(xhr.response).message;
                msg.style.color = "red";
            }
            else if (xhr.status === 422){
                msg.textContent = "Для таких действий нужно войти....";
                msg.style.color = "red";
            }
            else {
                msg.textContent = `Неизвестная ошибка со статусом ${xhr.status}`;
                msg.style.color = "red";
            }
        };
        xhr.send(formData);
    });

let sidebar_buttons = document.getElementsByClassName("sidebar-menu-button");
for (let i = 0; i < sidebar_buttons.length; i++){
    if (!sidebar_buttons.item(i).hasAttribute("data-target"))
        continue;
    let target = sidebar_buttons.item(i).getAttribute('data-target');
    if (!sections.hasOwnProperty(target))
        continue;
    if (sections[target]["permission"] > user_role){
        sidebar_buttons.item(i).style.display = 'none';
    }
    sidebar_buttons.item(i).addEventListener('click', function() {
        if (!sections.hasOwnProperty(target))
            return;
        menu_button(target, user_role);
      });
}
document.getElementById("page-comment-last").addEventListener("click", function (ev) {
    ev.preventDefault();
    if (page_current - 1 < 0)
        return;
    page_current -= 1;
    urlParameters.set("_p", page_current);
    history.replaceState(null, null, "?" + urlParameters.toString());
    get_user_comment(page_load_limit, page_current * page_load_limit);
})
document.getElementById("page-comment-next").addEventListener("click", function (ev) {
    ev.preventDefault();
    if (page_current + 1 < 0 || page_current + 1 >= page_count)
        return;
    page_current += 1;
    urlParameters.set("_p", page_current);
        history.replaceState(null, null, "?" + urlParameters.toString());
    get_user_comment(page_load_limit, page_current * page_load_limit);
})
document.getElementById("page-likes-last").addEventListener("click", function (ev) {
    ev.preventDefault();
    if (page_current - 1 < 0)
        return;
    page_current -= 1;
    urlParameters.set("_p", page_current);
    history.replaceState(null, null, "?" + urlParameters.toString());
    get_user_likes(page_load_limit, page_load_limit * page_current);
})
document.getElementById("page-likes-next").addEventListener("click", function (ev) {
    ev.preventDefault();
    if (page_current + 1 < 0 || page_current + 1 >= page_count)
        return;
    page_current += 1;
    urlParameters.set("_p", page_current);
        history.replaceState(null, null, "?" + urlParameters.toString());
    get_user_likes(page_load_limit, page_current * page_load_limit);
})
// urlParameters.set("_section", "comment");
// history.replaceState(null, null, "?" + urlParameters.toString());
if (urlParameters.has("_section")) {
    if (urlParameters.has("_p"))
        page_current = Number(urlParameters.get("_p"));
    last_section = urlParameters.get("_section").toString();
    menu_button(urlParameters.get("_section").toString(), page_current);
}
else
    menu_button("comments", reload=true);
// location.reload()