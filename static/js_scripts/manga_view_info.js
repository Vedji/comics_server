const __manga_name = window.location.pathname.split('/')[2];
let SCROLL_PROGRESS_COMMENTS = 0;
let SCROLL_ITEMS_ADD = 30;
let user_like_button = document.getElementById("user-like-manga-button");

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

function setToPageWorkInfo(work_id) {
    let url_work_info = `/api/v1/work/${work_id}`;
    fetch(url_work_info).then(response => {
        if (!response.ok) { throw new Error('Network response was not ok'); }
        return response.json();
    }).then(data => {
        if (data["status"] === "success"){
            document.getElementById("manga_name").textContent = data["data"]["ru_name"];
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
                'Authorization': `Bearer ${access_token}`
            }
        }).then(response => {
            if (!response.ok){
                user_like_button.style.display = 'none';
            }
            return response.json()})
        .then(data => {
            if (data["status"] === "success"){
                if (data["data"]["user_like"])
                    user_like_button.innerHTML = "&#129655;";
                else
                    user_like_button.innerHTML = "&#129293;";
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

function addComment(){
    fetch('/api/catalog/manga/comments?name='
    + __manga_name+"&limit="+SCROLL_ITEMS_ADD+"&offset="+(SCROLL_PROGRESS_COMMENTS * SCROLL_ITEMS_ADD)
    ).then(function(response) {
        if (response.ok) {
            return response.json();
        }
    throw new Error('Ошибка запроса');
    }).then(function(responseText) {
        if (responseText["result"]){
            var manga_name = document.getElementById("comments-list");
            for (var i = 0; i < responseText["comments"].length; i++){
                html_text = '<div class="comment"><div class="comment-title">';
                html_text += '<p> ' + responseText["comments"][i]["user_name"] + ' </p>';
                html_text += '<p>' + responseText["comments"][i]["manga_rating"] + '</p></div>';
                html_text += '<div class="comment-body"><p>' + responseText["comments"][i]["comment"];
                html_text += '</p></div></div>'
                manga_name.innerHTML += html_text;
          }
        }
    }).catch(function(error) {
        console.log(error);
    });
}


SCROLL_PROGRESS_COMMENTS += 1;

let menuButtons = document.getElementsByClassName('menu-button');
let description = document.getElementById('description');
let chapters = document.getElementById('chapters');
let comments_page = document.getElementById('comments');
let comment_form = document.getElementById('comment-form');

for (let i = 0; i < menuButtons.length; i++) {
    menuButtons[i].addEventListener('click', function() {
    let target = this.getAttribute('data-target');
    if (target === 'description') {
        description.style.display = 'block';
        chapters.style.display = 'none';
        comments_page.style.display = 'none';
    }else if (target === 'chapters') {
        chapters.style.display = 'block';
        comments_page.style.display = 'none';
        description.style.display = 'none';
    } else if (target === 'comments') {
        chapters.style.display = 'none';
        comments_page.style.display = 'block';
        description.style.display = 'none';
        if (userIsLogin){
            comment_form.style.display = "block";
        }else{
            comment_form.style.display = "none";
        }
        console.log();
    } else {
        chapters.style.display = 'none';
        comments_page.style.display = 'none';
        description.style.display = 'none';
    }
      });
}

document.getElementById('user-like-manga-button')
    .addEventListener('click', function(e) {
    e.preventDefault();
    fetch(`/api/v1/user/likes/${__manga_name}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
            body: JSON.stringify({})
        }).then(response => {
            if (!response.ok){
                user_like_button.style.display = 'none';
            }
            return response.json()})
        .then(data => {
            if (data["status"] === "success"){
                if (data["data"]["user_like"])
                    user_like_button.innerHTML = "&#129655;";
                else
                    user_like_button.innerHTML = "&#129293;";
            }
        }).catch(error => {
            alert(error);
        });
});

document.getElementById('comment-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var textarea = this.querySelector('textarea');
    var commentText = textarea.value;
    var commentDiv = document.createElement('div');
    commentDiv.classList.add('comment');
    commentDiv.innerHTML = '<p>' + commentText + '</p>';
    document.querySelector('.comments-list').appendChild(commentDiv);
    textarea.value = '';
});

window.addEventListener('scroll', function() {
if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
    var comments_page = document.getElementById('comments');

    if (comments_page.style.display == "block"){
        console.log(comments_page.style.display);
        addComment();
        SCROLL_PROGRESS_COMMENTS += 1;
    }
}
});


setToPageWorkInfo(__manga_name);
setChaptersWorks(__manga_name);