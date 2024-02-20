var __manga_name = window.location.pathname.split('/')[2];
var userIsLogin = false;
var SCROLL_PROGRESS_COMMENTS = 0;
var SCROLL_ITEMS_ADD = 30;


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

function getCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1, c.length);
    }
    if (c.indexOf(nameEQ) === 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
}

var data = {
    user_login: getCookie("user_login"),
    user_password: getCookie("user_password")
};

function setImage(image_id, file_id){
    var imageElement = document.getElementById(image_id);
    var description = document.getElementById('description');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/get_file?file_id=' + file_id, true);
    xhr.responseType = 'blob';
    xhr.onload = function() {
      if (xhr.status === 200) {
        var blob = xhr.response;
        var url = URL.createObjectURL(blob);
        imageElement.src = url;

      }
    };
    xhr.send();
}

fetch("/api/catalog/manga/is_read", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({"user_login": data.user_login,"user_password": data.user_password, "manga_name": __manga_name})
}).then(response => response.json()).then(data => {
    var username = document.getElementById("user_login");
    if (data["result"]){
        var chapters_list = document.getElementById("user-like-manga-button");
        if (data["manga_in_user_manga_like_list"]){
            chapters_list.innerHTML = "&#129655;";
        }else{
            chapters_list.innerHTML = "&#129293;";
        }
    }else{
        username.href = "/login";
    }
}).catch(error => {
  alert(error);
});


addComment();
SCROLL_PROGRESS_COMMENTS += 1;
fetch("/api/user/user_info", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
}).then(response => response.json())
.then(data => {
    var username = document.getElementById("user_login");
  if (data["result"]){
    username.text = data["user_name"];
    username.href = "/user/" + data["user_name"] + "/";
    userIsLogin = true;
  }else{
    username.href = "/login";
  }
})
.catch(error => {
  alert(error);
});

fetch('/api/catalog/info?name=' + __manga_name)
  .then(function(response) {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Ошибка запроса');
  })
  .then(function(responseText) {
    if (responseText["result"]){
        setImage("manga_title_image", responseText["manga_title_image"]);
        var manga_name = document.getElementById("manga_name");
        var manga_decs = document.getElementById('manga_description');
        manga_name.innerHTML = responseText["rus_manga_name"];
        manga_decs.innerHTML = responseText["manga_description"];
    }
  })
  .catch(function(error) {
    console.log(error);
});

function toChapter(url_chapter){
    location.href = url_chapter;
}

fetch('/api/catalog/chapters?name=' + __manga_name)
  .then(function(response) {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Ошибка запроса');
  })
  .then(function(responseText) {
    if (responseText["result"]){
        let chapters_list = document.getElementById("chapter-list");
        for (let i = 0; i < responseText["list_manga_chapters"].length; i++){
            let url_chapter = '/catalog_manga/' + __manga_name;
            url_chapter += '/read?c='+responseText["list_manga_chapters"][i]["chapter_number"] + '&p=1';
            let html_item = '<div class="chapter-element" onclick="';
            html_item += "toChapter('" + url_chapter + "')";
            html_item += '"><a class="chapter-href"> ' + responseText["list_manga_chapters"][i]["chapter_name"] + ' </a>';
            html_item += '</div>'
            chapters_list.innerHTML += html_item;
        }
    }
  })
  .catch(function(error) {
    console.log(error);
});



var menuButtons = document.getElementsByClassName('menu-button');
var description = document.getElementById('description');
var chapters = document.getElementById('chapters');
var comments_page = document.getElementById('comments');
var comment_form = document.getElementById('comment-form');

for (var i = 0; i < menuButtons.length; i++) {
    menuButtons[i].addEventListener('click', function() {
    var target = this.getAttribute('data-target');
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

var isReadButton = document.getElementById('user-like-manga-button');
isReadButton.addEventListener('click', function(e) {
    e.preventDefault();
    fetch("/api/catalog/manga/set_read", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(
    {"user_login": data.user_login,"user_password": data.user_password, "manga_name": __manga_name})})
    .then(response => response.json()).then(data => {
        var username = document.getElementById("user_login");
        if (data["result"]){
        var chapters_list = document.getElementById("user-like-manga-button");
        if (data["manga_in_user_like_manga"]){
            chapters_list.innerHTML = "&#129655;";
        }else{
            chapters_list.innerHTML = "&#129293;";
        }
        }else{
            username.href = "/login";
        }
    }).catch(error => {
        alert(error);
    });
});

var commentForm = document.getElementById('comment-form');
var commentsList = document.querySelector('.comments-list');

commentForm.addEventListener('submit', function(e) {
    e.preventDefault();
    var textarea = this.querySelector('textarea');
    var commentText = textarea.value;
    var commentDiv = document.createElement('div');
    commentDiv.classList.add('comment');
    commentDiv.innerHTML = '<p>' + commentText + '</p>';
    commentsList.appendChild(commentDiv);
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