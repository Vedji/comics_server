const __manga_name = window.location.pathname.split('/')[2];
let SCROLL_PROGRESS_COMMENTS = 0;
let SCROLL_ITEMS_ADD = 15;
let user_like_button = document.getElementById("user-like-manga-button");
let user_role = 0;
try { user_role = USER_ROLE; }catch (error){ console.log("USER_ROLE's not initialization"); }
let sections = {
    "description": {
        "permission": 0,
        "elements": [document.getElementById('description')],
        "elements_permission": [0]
    },
    "chapters": {
        "permission": 0,
        "elements": [document.getElementById('chapters')],
        "elements_permission": [0]
    },
    "comments": {
        "permission": 0,
        "elements": [document.getElementById('comments-list')],
        "elements_permission": [0]
    },
    "tools": {
        "permission": 1,
        "elements": [
            document.getElementById("tools-add-chapter-page"),
            document.getElementById("tools-del-work")
        ],
        "elements_permission": [1, 2]
    }
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
function check_user_like_work(user_like_exists) {
    user_like_button.style.display = 'block';
    if (user_like_exists) {
        user_like_button.innerHTML = "&#129655;";
        user_like_button.style.background = "rgba(255,0,0,0.56)";
    }
    else {
        user_like_button.innerHTML = "&#129293;";
        user_like_button.style.background = "rgba(133,27,171,0.6)";
    }

}
function setToPageWorkInfo(work_id) {
    let url_work_info = `/api/v1/work/${work_id}`;
    fetch(url_work_info).then(response => {
        if (!response.ok) { throw new Error('Network response was not ok'); }
        return response.json();
    }).then(data => {
        if (data["status"] === "success"){
            document.getElementById("manga_name").textContent = data["data"]["ru_name"].toString();
            document.getElementById('manga_description').textContent = data["data"]["desc"];
            let container_genres = document.getElementById("media-genres-list");
            if (data["data"]["genre_headers"].length === 0){
                container_genres.style.display = "none";
            }
            for (let item in data["data"]["genre_headers"]){
                let element = document.createElement("p");
                element.textContent = data["data"]["genre_headers"][item];
                container_genres.appendChild(element);
            }
            setImage("manga_title_image", data["data"]["pre_img"]);
        }
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });

    // Set user like button
    fetch(`/api/v1/user/likes/${__manga_name}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${ACCESS_TOKEN}`
    }}).then(response => {
        if (response.status === 401){
        }
        user_like_button.style.display = 'none';
        return response.json()})
    .then(data => {

        if (data["status"] === "success"){
            check_user_like_work(data["data"]["user_like"]);
        }
    }).catch(error => {
        alert(error);
    });
}
function setChaptersWorks(work_id) {
    let url_work_info = `/api/v1/work/${work_id}/chapter`;
    fetch(url_work_info).then(response => {
        if (!response.ok) { throw new Error('Network response was not ok'); }
        return response.json();
    }).then(data => {
        let chapters_container = document.getElementById("chapter-list");
        if (data["status"] === "success"){
            if (data["data"]["chapters_list"].length === 0){
                let message = document.createElement("p");
                message.textContent = "У этого произведения глав нету:(";
                chapters_container.appendChild(message);
            }
            for (let i in data["data"]["chapters_list"]){
                let chapter = document.createElement("a");
                let chapter_url =
                    `/catalog_manga/${__manga_name}/read?c=${data["data"]["chapters_list"][i]["chapter_number"]}&p=1`;
                chapter.setAttribute("class", "chapter-element");
                chapter.setAttribute("href", chapter_url);
                chapter.textContent = data["data"]["chapters_list"][i]["chapter_name"];
                chapters_container.appendChild(chapter);
            }
        }
        if (data["status"] === "error" && data["code"] === 404){
            let message = document.createElement("p");
                message.textContent = data["message"];
                chapters_container.appendChild(message);
        }
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
function isUserComment(visible = false) {
    let add_comm = document.getElementById("add-comment");
    let see_comm = document.getElementById("user-comment-container");
    let edit_comm = document.getElementById("edit-comment-container");
    edit_comm.style.display = 'none';
    if (!visible){
        add_comm.style.display = 'none';
        see_comm.style.display = 'none';
        return;
    }
    let url = `/api/v1/user/comments/${__manga_name}`;
    fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${ACCESS_TOKEN}`},
    }).then(response => response.json()).then(data => {
        if (data["status"] === "success"){
            if (data["data"]["comment_exists"]) {
                add_comm.style.display = 'none';
                see_comm.style.display = 'block';
                let title = document.getElementById("user-comment-range");
                title.textContent = `Оценка ${data["data"]["rating"]}`;
                let text = document.getElementById("user-comment-text");
                text.textContent = data["data"]["comment"];
                let edit_text = document.getElementById("edit-comment-container-text");
                edit_text.textContent = data["data"]["comment"];
                let edit_rating = document.getElementById("editMyRangeValue");
                edit_rating.setAttribute("value", data["data"]["rating"]);
                let show_edit_rating = document.getElementById("showEditMyRangeValue");
                show_edit_rating.textContent = `Оценка: ${data["data"]["rating"]}`;
            }else{
                add_comm.style.display = 'block';
                see_comm.style.display = 'none';
            }
        }
    }).catch(error => {
        alert(error);
    });
}
function addComment(limit = -1, offset = 0){
    let comment_list_container = document.getElementById("comments-list-body");
    if (offset === 0){
        let divs = comment_list_container.querySelectorAll(".comments-list-body");
        for (let i = divs.length - 1; i >= 0; i--)
            comment_list_container.removeChild(divs[i]);
    }
    let params = {
        limit: limit,
        offset: offset,
        but_user_id: USER_ID
    }
    let paramToURL = new URLSearchParams(params).toString();
    let url = `/api/v1/work/${__manga_name}/comments?${paramToURL}`;
    fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json'},
    }).then(response => response.json()).then(data => {
        if (data["status"] === "success"){
            for(let i = 0; i < data["data"]["comments-list"].length; i++){
                let comment_container = document.createElement("div");
                comment_container.setAttribute("class", "comments-list-body");
                let head = document.createElement("div");
                head.setAttribute("class", "comments-list-body-element-head");
                let h3 = document.createElement("h3");
                h3.textContent = data["data"]["comments-list"][i]["username"];
                if (USERNAME === data["data"]["comments-list"][i]["username"]){
                    h3.textContent = "> " + h3.textContent + " <";
                    h3.style.color = "#FF9640";
                }
                head.appendChild(h3);
                let p = document.createElement("p");
                p.textContent = `Оценка ${data["data"]["comments-list"][i]["rating"]}`;
                head.appendChild(p);
                comment_container.appendChild(head);
                let body = document.createElement("div");
                body.setAttribute("class", "comments-list-body-text");
                p = document.createElement("p");
                p.textContent = data["data"]["comments-list"][i]["comment"];
                body.appendChild(p);
                comment_container.appendChild(body);
                comment_list_container.appendChild(comment_container);
            }
        }
    }).catch(error => {
        alert(error);
    });
}
function draggable(e) {
    let listItems = document.querySelectorAll('.tools-add-chapter-page-container-files-show-dad-list-element');
    let draggedItem = null;
    for (let item of listItems) {

        item.addEventListener('dragstart', function() {
            draggedItem = item;
            setTimeout(() => {
                item.style.display = 'none';
                e.target.style.opacity = '1';
            }, 0);
        });

        item.addEventListener('dragend', function() {
            setTimeout(() => {
                draggedItem.style.display = 'block';
                e.target.style.opacity = '1';
                draggedItem = null;
            }, 0);
        });

        item.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.target.style.opacity = '1';
        });

        item.addEventListener('dragenter', function(e) {
            e.preventDefault();
            e.target.style.opacity = '1';
        });

        item.addEventListener('drop', function(e) {
            let rect = item.getBoundingClientRect();
            if (!draggedItem)
                return;
            console.log(draggedItem);
            if (rect.height / 2 > e.offsetY)
                this.before(draggedItem);
            else
                this.after(draggedItem);
        });
    }
}


function input_menu(target, per = 0) {
    for (let item in sections){
        if (!sections.hasOwnProperty(item))
            continue;
        if (item === target && per >= sections[item]["permission"]) {
            for (let i = 0; i < sections[item]["elements"].length; i++){
                if (i >= sections[item]["elements_permission"].length)
                    continue;
                if (per < sections[item]["elements_permission"][i])
                    continue;
                sections[item]["elements"][i].style.display = 'block';
            }
            continue;
        }
        for (let i = 0; i < sections[item]["elements"].length; i++) {
            sections[item]["elements"][i].style.display = 'none';
        }
    }
    isUserComment();
    if (target === "description"){
        return;
    }
    if (target === "chapters"){
        return;
    }
    if (target === "comments"){
        addComment(SCROLL_ITEMS_ADD, SCROLL_PROGRESS_COMMENTS * SCROLL_ITEMS_ADD);
        SCROLL_PROGRESS_COMMENTS += 1
        document.getElementById("add-comment").style.display = 'none';
        isUserComment(true);
        return;
    }
    if (target === "tools"){
        return;
    }
}

function setNeedLoadImage() {
    let items = document.querySelectorAll(".tools-add-chapter-page-container-files-show-dad-list-element");
    let container = document.getElementById("tools-add-chapter-page-container-files-show-dad-list");
    if (items.length === 0){
        let cont = document.createElement("div");
        cont.style.display = 'flex';
        cont.style.justifyContent = 'center';
        let p = document.createElement("p");
        p.textContent = "Надо бы чего нить загрузить -_- ";
        cont.appendChild(p);
        container.appendChild(cont);
    }
}

document.getElementById('user-like-manga-button')
    .addEventListener('click', function(e) {
    e.preventDefault();
    fetch(`/api/v1/user/likes/${__manga_name}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${ACCESS_TOKEN}`
            },
            body: JSON.stringify({})
        }).then(response => {
            if (!response.ok){
                user_like_button.style.display = 'none';
            }
            return response.json()})
        .then(data => {
            if (data["status"] === "success"){
                check_user_like_work(data["data"]["user_like"]);
            }
        }).catch(error => {
            alert(error);
        });
});

document.getElementById("edit-comment-form").addEventListener('submit', function (e) {
    e.preventDefault();
    let rating = document.getElementById("editMyRangeValue");
    let comment = document.getElementById("edit-comment-container-text");

    fetch(`/api/v1/user/comments/${__manga_name}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${ACCESS_TOKEN}`
            },
            body: JSON.stringify({
                rating: rating.value,
                comment: comment.value
            })
        })
        .then(response => {
            isUserComment(true);
            if (response.status === 401)
                alert("No permision");
            return response.json()
        })
        .then(data => {
            if (data["status"] === "success") {
                isUserComment(true);
                addComment(SCROLL_ITEMS_ADD, 0);
                SCROLL_PROGRESS_COMMENTS = 1
            }
        })
        .catch(error => console.error(error));
})

document.getElementById("to-edit-user-comment").addEventListener("click", function (e) {
    e.preventDefault();
    let latest_container = document.getElementById("user-comment-container");
    let new_container = document.getElementById("edit-comment-container");
    latest_container.style.display = 'none';
    new_container.style.display = 'block';
    let cur_rating = document.getElementById("user-comment-range");
    let cur_comment = document.getElementById("user-comment-text");
    let rating = document.getElementById("editMyRangeValue");
    let comment = document.getElementById("edit-comment-container-text");
    rating.value = cur_rating.textContent.split(":")[-1];
    comment.value = cur_comment.textContent;
})

document.getElementById("btn-cancel-edit-user-comment").addEventListener("click", function (e) {
    e.preventDefault();
    let latest_container = document.getElementById("user-comment-container");
    let new_container = document.getElementById("edit-comment-container");
    latest_container.style.display = 'block';
    new_container.style.display = 'none';
})

document.getElementById("user-comment-container-btn-del")
    .addEventListener("click", function (e) {
        e.preventDefault();
        fetch(`/api/v1/user/comments/${__manga_name}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${ACCESS_TOKEN}`
            }
        })
        .then(response => {
            isUserComment(true);
            if (response.status === 401)
                alert("No permision");
            return response.json()
        })
        .then(data => {
            if (data["status"] === "success") {
                isUserComment(true);
                addComment(SCROLL_ITEMS_ADD, 0);
                SCROLL_PROGRESS_COMMENTS = 1
            }
        })
        .catch(error => console.error(error));
})

document.getElementById('add-comment').addEventListener('submit', function(e) {
    e.preventDefault();
    let rating = document.getElementById("myRange");
    let comment = document.getElementById("add-comment-input-text");
    fetch(`/api/v1/user/comments/${__manga_name}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${ACCESS_TOKEN}`
        },
        body: JSON.stringify({
            comment: comment.value,
            rating: rating.value
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
            isUserComment(true);
            addComment(SCROLL_ITEMS_ADD, 0);
            SCROLL_PROGRESS_COMMENTS = 1
        }
    })
    .catch(error => console.error(error));
});

window.addEventListener('scroll', function() {
if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
    let comments_page = document.getElementById('comments-list');
    if (comments_page.style.display === "block"){
        console.log(comments_page.style.display);
        addComment(SCROLL_ITEMS_ADD, SCROLL_PROGRESS_COMMENTS * SCROLL_ITEMS_ADD);
        SCROLL_ITEMS_ADD += 1;
        SCROLL_PROGRESS_COMMENTS += 1;
    }
}
});

document.getElementById("myRange").addEventListener('input', function () {
    let p = document.getElementById("myRangeValue");
    p.textContent = ` Оценка: ${this.value} `;
})

document.getElementById("editMyRangeValue")
    .addEventListener('input', function () {
    let p = document.getElementById("showEditMyRangeValue");
    p.textContent = ` Оценка: ${this.value} `;
})

document.getElementById("tools-add-chapter-page-container-form-files")
    .addEventListener("change", function (e) {
        let files = e.target.files;
        if (files.length === 0){
            let p = document.createElement("p");
            p.textContent = "Упс, загрузите файлы"
            document.getElementById("tools-add-chapter-page-container-files-show-dad-list").appendChild(p)
        }
        let container = document.getElementById("tools-add-chapter-page-container-files-show-dad-list");
        container.innerHTML = "";

        for (let i = 0; i < files.length; i++){
            if (!files[i])
                continue;
            let li = document.createElement("li");
            li.setAttribute("class", "tools-add-chapter-page-container-files-show-dad-list-element");
            li.draggable = true;
            let cont = document.createElement("div");

            let reader = new FileReader();
            let img = document.createElement("img");
            img.width = 100;
            img.height = 150;
            img.setAttribute("draggable", "false");
            img.setAttribute("data-img-name", files[i].name)
            reader.onload = function (r) {
                img.src =  r.target.result;
            }
            reader.readAsDataURL(files[i]);
            cont.appendChild(img);
            let p = document.createElement("p");
            p.textContent = files[i].name;
            cont.appendChild(p);
            let btn = document.createElement("button");
            btn.class = "tools-add-chapter-page-container-files-show-dad-list-element";
            btn.textContent = "DELETE";
            btn.setAttribute("class", "temp-button")
            btn.onclick = function (ev) {
                ev.preventDefault();
                img.src = "";
                container.removeChild(li);
                setNeedLoadImage();
            }
            cont.appendChild(btn);
            li.appendChild(cont);
            container.appendChild(li);
            draggable(event);
        }
    })

document.getElementById("tools-add-chapter-page-container-form-data").addEventListener("submit", function (ev) {
    ev.preventDefault();
    let file_storage = document.getElementById("tools-add-chapter-page-container-form-files");
    let files_to_sand = [];
    let msg = document.getElementById("tools-add-chapter-page-msg");
    function findFileByName(fileList, fileName) {
        for (let i = 0; i < fileList.length; i++) {
            if (fileList[i].name === fileName) {
                return fileList[i];
            }
        }
        return null;
    }
    let file_item = document.querySelectorAll(".tools-add-chapter-page-container-files-show-dad-list-element");
    for (let i = 0; i < file_item.length; i++){
        let container = file_item[i].getElementsByTagName("div").item(0);
        let img = container.getElementsByTagName("img").item(0);
        let c_file = findFileByName(file_storage.files, img.getAttribute("data-img-name"))
        if (!c_file){
            msg.textContent = `Ошибка файла ${img.getAttribute("data-img-name")}`;
            return;
        }
        files_to_sand.push(c_file);
    }
    let post_url = `/api/v1/work/${__manga_name}/chapter`;
    let formData = new FormData();
    formData.append("chapter_name", document.getElementById("tools-add-chapter-page-container-form-name").value);
    formData.append("chapter_num", document.getElementById("tools-add-chapter-page-container-form-num").value);
    formData.append("count_files", files_to_sand.length);
    for (let i = 0; i < files_to_sand.length; i++ ){
        formData.append(`file_${i}`, files_to_sand[i])
    }

    let xhr = new XMLHttpRequest();
    xhr.open('POST', post_url, true);
    xhr.setRequestHeader("Authorization", `Bearer ${ACCESS_TOKEN}`);
    xhr.onload = function () {
        if (xhr.status === 200) {
            msg.textContent = "Глава успешно загружена";
            msg.style.color = "green";
        }
        else if (xhr.status === 400 || xhr.status === 401){
            msg.textContent = JSON.parse(xhr.response).message;
            msg.style.color = "red";
        }
        else if (xhr.status === 422){
            msg.textContent = "Для таких действий нужно войти....";
            msg.style.color = "red";
        }else if (xhr.status === 405){
            msg.textContent = `[${xhr.status}]: Это же не дело, вот так добавлять главы куда попало(((`;
            msg.style.color = "red";
        }
        else {
            msg.textContent = `Неизвестная ошибка со статусом ${xhr.status}`;
            msg.style.color = "red";
        }
    };
    xhr.send(formData);

})

document.getElementById("tools-del-work-body-btn-del")
    .addEventListener("click", function (e) {
        e.preventDefault();
        let checkbox = document.getElementById("tools-del-work-body-btn-del-check")
        if (checkbox.getAttribute("data-checked") === "false")
            return;
        fetch(`/api/v1/work/${__manga_name}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${ACCESS_TOKEN}`
            }
        })
        .then(response => {
            isUserComment(true);
            if (response.status === 401)
                alert("No permision");
            return response.json()
        })
        .then(data => {})
        .catch(error => console.error(error));
        location.href = "/";
    })

document.getElementById("tools-del-work-body-btn-del-check")
    .addEventListener("click", function (ev) {
    ev.preventDefault();
    if (this.getAttribute("data-checked") === "false"){
        this.textContent = "x";
        this.setAttribute("data-checked", "true");
    }else{
        this.textContent = "";
        this.setAttribute("data-checked", "false");
    }
    console.log(this.getAttribute("data-checked"));
})


let menuButtons = document.getElementsByClassName('menu-button');
for (let i = 0; i < menuButtons.length; i++) {
    if (!menuButtons.item(i).hasAttribute('data-target'))
            continue;
        let target = menuButtons.item(i).getAttribute('data-target');
        if (sections[target]["permission"] > user_role){
            menuButtons.item(i).style.display = "none";
            continue;
        }
    menuButtons[i].addEventListener('click', function() { input_menu(target, user_role); });
}
setToPageWorkInfo(__manga_name);
setChaptersWorks(__manga_name);
setNeedLoadImage();

input_menu("chapters");
input_menu("description");
