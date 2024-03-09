const SVG_ICON_UNLIKE   = '<svg class="manager-group-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M47.6 300.4L228.3 469.1c7.5 7 17.4 10.9 27.7 10.9s20.2-3.9 27.7-10.9L464.4 300.4c30.4-28.3 47.6-68 47.6-109.5v-5.8c0-69.9-50.5-129.5-119.4-141C347 36.5 300.6 51.4 268 84L256 96 244 84c-32.6-32.6-79-47.5-124.6-39.9C50.5 55.6 0 115.2 0 185.1v5.8c0 41.5 17.2 81.2 47.6 109.5z"/></svg>';
const SVG_ICON_LIKE = '<svg class="manager-group-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M225.8 468.2l-2.5-2.3L48.1 303.2C17.4 274.7 0 234.7 0 192.8v-3.3c0-70.4 50-130.8 119.2-144C158.6 37.9 198.9 47 231 69.6c9 6.4 17.4 13.8 25 22.3c4.2-4.8 8.7-9.2 13.5-13.3c3.7-3.2 7.5-6.2 11.5-9c0 0 0 0 0 0C313.1 47 353.4 37.9 392.8 45.4C462 58.6 512 119.1 512 189.5v3.3c0 41.9-17.4 81.9-48.1 110.4L288.7 465.9l-2.5 2.3c-8.2 7.6-19 11.9-30.2 11.9s-22-4.2-30.2-11.9zM239.1 145c-.4-.3-.7-.7-1-1.1l-17.8-20c0 0-.1-.1-.1-.1c0 0 0 0 0 0c-23.1-25.9-58-37.7-92-31.2C81.6 101.5 48 142.1 48 189.5v3.3c0 28.5 11.9 55.8 32.8 75.2L256 430.7 431.2 268c20.9-19.4 32.8-46.7 32.8-75.2v-3.3c0-47.3-33.6-88-80.1-96.9c-34-6.5-69 5.4-92 31.2c0 0 0 0-.1 .1s0 0-.1 .1l-17.8 20c-.3 .4-.7 .7-1 1.1c-4.5 4.5-10.6 7-16.9 7s-12.4-2.5-16.9-7z"/></svg>';
const SVG_ICON_TRASH = '<svg class="work-chapter-delete-icon"  xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg>';

const PERMISSION_TO_DELETE_CHAPTER = 2;
const WORK_ID = window.location.pathname.split('/')[2];
const first_init_layout = "section-info";
let current_layout = first_init_layout;

let last_execute_comment_count = 0;
let last_comment = undefined;
let comment_page_limit = 10;
let comment_page_offset = 0;
let first_chapter = undefined;
let access_token = undefined;
let user_role = 0;
let username = undefined;
let user_id = undefined;
try { user_role = USER_ROLE; }catch (error){ console.log("USER_ROLE's not initialization"); }
try { access_token = ACCESS_TOKEN; }catch (error){ console.log("user not initialization, not ACCESS_TOKEN"); }
try { username = USERNAME; }catch (error){ console.log("user not authorization, not USERNAME"); }
try { user_id = USER_ID; }catch (error){ console.log("user not authorization, not USER_ID"); }
let _sections = document.getElementsByClassName("pag-nav-item");
console.log(username, user_role);
let nav_menu = {
    "section-info": {
        "layouts": [document.getElementById("section-description-layout")]
    },
    "section-chapters": {
        "layouts": [document.getElementById("section-chapters-layout")]
    },
    "section-comments": {
        "layouts": [document.getElementById("section-comments-layout")]
    }
}

function set_user_comments() {
    // set work add comment, if comment isn't exists
    let add_comm = document.getElementById("comment-add-form");
    let see_comm = document.getElementById("self-comment-see-container");
    let edit_comm = document.getElementById("comment-edit-form");
    edit_comm.style.display = 'none';
    add_comm.style.display = 'none';
    see_comm.style.display = 'none';
    let url = `/api/v1/user/comments/${WORK_ID}`;
    fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${ACCESS_TOKEN}`},
    }).then(response => response.json()).then(data => {
        if (data["status"] === "success"){
            let comment = data["data"]["comment"];
            if (data["data"]["comment_exists"]) {
                see_comm.style.display = 'block';
                document.getElementById("self-comment-see-text").textContent = comment;
                document.getElementById("comments-layout-input-set").value = comment;
                document.getElementById("comment-see-edit").addEventListener('click', function (ev) {
                    ev.preventDefault();
                    edit_comm.style.display = 'block';
                    add_comm.style.display = 'none';
                    see_comm.style.display = 'none';
                });
                document.getElementById("comment-see-delete").addEventListener('click',
                    () => {
                    edit_comm.style.display = 'none';
                    add_comm.style.display = 'block';
                    see_comm.style.display = 'none';
                    delete_user_comment(user_id);
                });
                document.getElementById("comment-set-undo").addEventListener("click", function (ev) {
                    edit_comm.style.display = 'none';
                    add_comm.style.display = 'none';
                    see_comm.style.display = 'block';
                    document.getElementById("comments-layout-input-set").value = comment;
                })
                return;
            }
            add_comm.style.display = 'block';
        }
    }).catch(error => {
        alert(error);
    });
}

function delete_user_comment(deleted_id_comment) {
    let url = `/api/v1/user/comments/${WORK_ID}?${
        (new URLSearchParams({user_id: deleted_id_comment}).toString())}`
    fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${access_token}`
            }
        })
        .then(response => {
            if (response.status === 401)
                alert("No permision");
            return response.json()
        })
        .then(data => {
            if (data["status"] === "success") {

                if (user_id === deleted_id_comment){
                    document.getElementById("comment-add-form").style.display = 'block';
                    document.getElementById("self-comment-see-container").style.display = 'none';
                    document.getElementById("comment-edit-form").style.display = 'none';
                }
                if (user_id !== deleted_id_comment){

                    let comms = document.getElementById("comments-list").children;
                    for (let i = comms.length - 1; i >= 0; i--){
                        console.log("Comment deleted 3", comms[i]);
                        if (!comms.item(i).hasAttribute("data-user-id"))
                            continue;
                        if (comms.item(i).getAttribute("data-user-id") !== deleted_id_comment.toString())
                            continue;
                        console.log("Comment deleted 2", deleted_id_comment);
                        document.getElementById('comments-list').removeChild(comms.item(i));
                    }
                }
            }
        })
        .catch(error => console.error(error));
}
function addComment(limit = -1, offset = 0){
    let comment_list_container = document.getElementById("comments-list");
    if (offset === 0){
        comment_list_container.innerHTML = '';
    }
    comment_page_offset += 1;
    let params = {
        limit: limit.toString(),
        offset: offset.toString()
    }
    let url = `/api/v1/work/${WORK_ID}/comments?${(new URLSearchParams(params)).toString()}`;
    fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json'},
    }).then(response => response.json()).then(data => {
        if (data["status"] === "success"){
            last_execute_comment_count = data["data"]["comments-list"].length;
            for(let i = 0; i < data["data"]["comments-list"].length; i++){
                if (username === data["data"]["comments-list"][i]["username"])
                    continue;
                let div1 = document.createElement("div");
                div1.setAttribute("class", "comment-two-buttons comment-item-head");
                div1.setAttribute("data-user-id", data["data"]["comments-list"][i]["user_id"]);
                let h2 = document.createElement("h2");
                h2.setAttribute("class", "all-comments-item-header");
                h2.textContent = data["data"]["comments-list"][i]["username"];
                div1.appendChild(h2);
                let p = document.createElement("p");
                if (user_role > 1) {
                    let div2 = document.createElement("div");
                    div2.setAttribute("class", "comments-item-trash");
                    div2.innerHTML = SVG_ICON_TRASH;
                    div1.appendChild(div2);


                    let usr = data["data"]["comments-list"][i]["user_id"].toString();
                    div2.addEventListener('click', () => {
                        console.log("Comment deleted", usr);
                        delete_user_comment(usr);
                    });
                }
                comment_list_container.appendChild(div1);
                p.setAttribute("data-user-id", data["data"]["comments-list"][i]["user_id"]);
                p.setAttribute("class", "see-all-comments-item-text");
                p.textContent = data["data"]["comments-list"][i]["comment"];
                comment_list_container.appendChild(p);
                last_comment = p;
                let line_sep = document.createElement("div");
                line_sep.setAttribute("class", "comment-line-split");
                comment_list_container.appendChild(line_sep);
            }
        }
    }).catch(error => {
        alert(error);
    });
}

function setImage(image_id, file_id){
    let imageElement = document.getElementById(image_id);
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `/api/get_file?file_id=${file_id}`, true);
    xhr.responseType = 'blob';
    xhr.onload = function() {
      if (xhr.status === 200) {
        imageElement.src = URL.createObjectURL(xhr.response);
      }
    };
    xhr.send();
}

function update_user_like_icon(is_like, auth = true) {
    let set_favorites_click = document.getElementById("set-favorites-click");
    let icon_like_container = document.getElementById("set-favorites-icon");
    let favorite_text = document.getElementById("set-favorites-p");
    if (!auth){
        set_favorites_click.style.visibility = 'hidden';
    }else{
        set_favorites_click.style.visibility = 'visibility';
    }
    icon_like_container.innerHTML = '';
    if (is_like){
        icon_like_container.innerHTML = SVG_ICON_LIKE;
        icon_like_container.style.background =
            'radial-gradient(123.00% 123.00% at 50% 50%, rgb(143 36 36), rgba(255, 255, 255, 0) 100%)';
        icon_like_container.style.border = '0.17rem solid rgb(150 0 0 / 86%)'
        favorite_text.textContent = "Понравилось";
    }else{
        icon_like_container.innerHTML = SVG_ICON_UNLIKE;
        icon_like_container.style.background =
            'radial-gradient(123.00% 123.00% at 50% 50%, rgb(255, 255, 255), rgba(255, 255, 255, 0) 100%)';
        icon_like_container.style.border = '0.17rem solid rgba(255, 255, 255, 0.59)';
        favorite_text.textContent = "В избранное";
    }
}
function setChaptersWorks(work_id) {
    let chapters_container = document.getElementById("work-chapters-list");
    chapters_container.innerHTML = '';
    let url_work_info = `/api/v1/work/${work_id}/chapter`;
    fetch(url_work_info).then(response => {
        if (!response.ok) { throw new Error('Network response was not ok'); }
        return response.json();
    }).then(data => {
        if (data["status"] === "success"){
            if (data["data"]["chapters_list"].length === 0){
                let msg = document.createElement("p");
                msg.textContent = 'Увы, глав нет :\'(';
                msg.setAttribute("class", "chapter-msg-no-items");
                chapters_container.appendChild(msg);
                let goto_chapter_button = document.getElementById("start-read-click");
                goto_chapter_button.style.visibility = "hidden";
            }
            for (let i in data["data"]["chapters_list"]){
                if (!first_chapter)
                    first_chapter = `/catalog_manga/${work_id}/read?c=${data["data"]["chapters_list"][i]["chapter_number"]}&p=1`
                let chapter_url =
                    `/catalog_manga/${work_id}/read?c=${data["data"]["chapters_list"][i]["chapter_number"]}&p=1`;
                let container = document.createElement("div");
                container.innerHTML = '';
                container.setAttribute("class", "work-chapter");
                let a = document.createElement("a");
                a.setAttribute("href", chapter_url);
                a.textContent = data["data"]["chapters_list"][i]["chapter_name"];
                container.appendChild(a);
                if (user_role >= PERMISSION_TO_DELETE_CHAPTER){
                    let trash = document.createElement("div");
                    trash.setAttribute("class", "work-chapter-trash");
                    trash.innerHTML += SVG_ICON_TRASH;
                    container.appendChild(trash);
                }
                chapters_container.appendChild(container);
            }
        }
        if (data["status"] === "error" && data["code"] === 404){
            let msg = document.createElement("p");
                msg.textContent = 'Ты как это сделал :\'(';
                msg.setAttribute("class", "chapter-msg-no-items");
                console.log(msg);
        }
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function section_navigation(section) {
    current_layout = section;
    for (let nav in nav_menu){
        for (let y = 0; y < nav_menu[nav]["layouts"].length; y++){
            if (nav === section){
                nav_menu[nav]["layouts"][y].style.display = "block";
            }else{
                nav_menu[nav]["layouts"][y].style.display = "none";
            }
        }
        if (nav === "section-comments"){
            set_user_comments();
            addComment(comment_page_limit, comment_page_limit * comment_page_offset);
        }
    }
}

function on_load_page(work_id) {
    let url_work_info = `/api/v1/work/${work_id}`;
    fetch(url_work_info).then(response => {
        if (!response.ok) { throw new Error('Network response was not ok'); }
        return response.json();
    }).then(data => {
        if (data["status"] === "success"){
            document.getElementById("work-name-text").textContent = data["data"]["ru_name"].toString();
            document.getElementById('work-description-text').textContent = data["data"]["desc"];
            let container_genres = document.getElementById("work-genres-container");
            if (data["data"]["genre_headers"].length === 0){
                container_genres.style.display = "none";
            }
            for (let item in data["data"]["genre_headers"]){
                let element = document.createElement("p");
                element.textContent = data["data"]["genre_headers"][item];
                element.setAttribute("class", "work-genre");
                container_genres.appendChild(element);
            }
            setImage("preview-image", data["data"]["pre_img"]);
        }
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
    // get chapters list

    setChaptersWorks(work_id);
    // Set user like button
    if (access_token === undefined)
        return;
    fetch(`/api/v1/user/likes/${work_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
    }}).then(response => {
        if (response.status !== 200)
            update_user_like_icon(false, false);
        return response.json()})
    .then(data => {
        if (data["status"] === "success"){
            update_user_like_icon(data["data"]["user_like"], true);
            console.log(data["data"]["user_like"])
        }
    }).catch(error => {
        alert(error);
    });
    // init user comment
    section_navigation(first_init_layout);
}
document.getElementById("set-favorites-click").addEventListener("click", function (ev) {
    ev.preventDefault();
    fetch(`/api/v1/user/likes/${WORK_ID}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
            body: JSON.stringify({})
        }).then(response => {
            if (!response.ok){
                update_user_like_icon(false, false);
            }
            return response.json()})
        .then(data => {
            if (data["status"] === "success"){
                update_user_like_icon(data["data"]["user_like"], true);
            }
        }).catch(error => {
            alert(error);
        });
});
document.getElementById("start-read-click").addEventListener("click", function (ev) {
    if (!first_chapter){
        return;
    }
    location.href = first_chapter;
})

for (let i = 0; i < _sections.length; i++){
    if (!_sections.item(i).hasAttribute("data-section"))
        continue;
    _sections.item(i).addEventListener("click", function (ev) {
        ev.preventDefault();
        section_navigation(_sections.item(i).getAttribute("data-section"));
        let bottom_line = document.getElementById("page-nav-line");
        let rect = _sections.item(i).getBoundingClientRect();
        bottom_line.style.left = `${rect.left}px`;
        bottom_line.style.bottom = `${rect.bottom}px`;
        bottom_line.style.width = `${rect.width}px`;
        bottom_line.style.top = `${rect.height}px`;
    })
    if (_sections.item(i).getAttribute("data-section") === first_init_layout)
        _sections.item(i).click();
}
window.addEventListener('scroll', function() {
    if (current_layout !== "section-comments")
        return;
    if (last_comment === undefined)
        return;
    if (last_execute_comment_count < comment_page_limit)
        return;

    let rect = last_comment.getBoundingClientRect();
    if (rect.top >= 0 && rect.bottom <= window.innerHeight){
        work_current_page += 1;
        addComment(comment_page_limit, comment_page_offset * comment_page_limit);
    }
});
document.getElementById('comment-add-form')
    .addEventListener('submit', function(e) {
        e.preventDefault();
        let comment = document.getElementById("comments-layout-input-new").value;
        fetch(`/api/v1/user/comments/${WORK_ID}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${access_token}`
            },
            body: JSON.stringify({
                comment: comment,
                rating: 7
            })
        })
        .then(response => {
            if (response.status === 409)
                isUserComment(true);
            else if (response.status === 400)
                alert(response.json()["message"]);
            return response.json()
        })
        .then(data => {
            if (data["status"] === "success") {
                document.getElementById("comment-add-form").style.display = 'none';
                document.getElementById("self-comment-see-container").style.display = 'block';
                document.getElementById("comment-edit-form").style.display = 'none';
                document.getElementById("self-comment-see-text").textContent = comment;
            }
        })
        .catch(error => console.error(error));
    });
document.getElementById("comment-edit-form")
    .addEventListener('submit', function (e) {
        e.preventDefault();
        let comment = document.getElementById("comments-layout-input-set").value;

        fetch(`/api/v1/user/comments/${WORK_ID}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": `Bearer ${access_token}`
                },
                body: JSON.stringify({
                    rating: 8,
                    comment: comment
                })
            }).then(response => {
                if (response.status === 401)
                    alert("No permision");
                return response.json()
            }).then(data => {
                if (data["status"] === "success") {
                    document.getElementById("comment-add-form").style.display = 'none';
                    document.getElementById("self-comment-see-container").style.display = 'block';
                    document.getElementById("comment-edit-form").style.display = 'none';
                    document.getElementById("self-comment-see-text").textContent = comment;
                }
            }).catch(error => console.error(error));
})


on_load_page(WORK_ID);