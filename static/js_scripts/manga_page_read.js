var __manga_name = window.location.pathname.split('/')[2];
var queryString = window.location.search;
var urlParams = new URLSearchParams(queryString);

var chapter = urlParams.get('c');
var page = urlParams.get('p');


function setImage(image_id, file_id){
    var imageElement = document.getElementById(image_id);
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

fetch('/api/catalog/manga/chapter?name=' + __manga_name + '&c=' + chapter)
.then(function(response) {
    if (response.ok) {
        return response.json();
    }
throw new Error('Ошибка запроса');})
.then(function(responseText) {
    if (responseText["result"]){

        if (responseText["chapter_len"] > 0){

            var ch_list = document.getElementById('valueList');
            for (var i = 2; i <= responseText["chapter_len"]; i++){
                var text = '<option value="' + i + '"> - ' + i +' - </option>';
                ch_list.innerHTML += text;
            }
            ch_list.value = page;
        }
    }else{
            location.href = '/catalog_manga/' + __manga_name + '/';
    }
})
.catch(function(error) {
    console.log(error);
});

fetch('/api/catalog/manga/page?name=' + __manga_name + '&c=' + chapter + '&p='+page).then(function(response) {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Ошибка запроса');
    }).then(function(responseText) {
        if (responseText["result"]){
            setImage("manga_page_img", responseText["id_page_image"]);
        }
    }).catch(function(error) {
        console.log(error);
    });

function prevView(){
    if(page > 1){

        location.href = '/catalog_manga/' + __manga_name + '/read?c=' + chapter + '&p=' + (page - 1);
    }
    fetch('/api/catalog/manga/chapter?name=' + __manga_name + '&c=' + (chapter - 1)).then(function(response) {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Ошибка запроса');
    }).then(function(responseText) {
        if (responseText["result"]){
            if (responseText["chapter_len"] > 0){
                location.href = '/catalog_manga/' + __manga_name + '/read?c=' + (chapter - 1) + '&p=' + (responseText["chapter_len"]);
            }
        }else{
                location.href = '/catalog_manga/' + __manga_name + '/';
        }
    }).catch(function(error) {
        console.log(error);
    });
}

function nextView(){
    fetch('/api/catalog/manga/chapter?name=' + __manga_name + '&c=' + chapter).then(function(response) {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Ошибка запроса');
        }).then(function(responseText) {
            if (responseText["result"]){
                if (responseText["chapter_len"] > page){
                    location.href = '/catalog_manga/' + __manga_name + '/read?c=' + chapter + '&p=' + ((page/1) + 1);
                }else{
                    fetch('/api/catalog/manga/chapter?name=' + __manga_name + '&c=' + ((chapter/1) + 1)).then(function(response) {
                        if (response.ok) {
                            return response.json();
                        }
                        throw new Error('Ошибка запроса');
                        }).then(function(responseText) {
                        if (responseText["result"]){
                                location.href = '/catalog_manga/' + __manga_name + '/read?c=' + ((chapter/1) + 1) + '&p=1';

                        }else{
                                location.href = '/catalog_manga/' + __manga_name + '/';
                        }
                        }).catch(function(error) {
                        console.log(error);
                        });
                }
            }else{
                    location.href = '/catalog_manga/' + __manga_name + '/';
            }
        }).catch(function(error) {
            console.log(error);
        });
}

var image = document.getElementById('manga_page_img');
image.addEventListener('click', function(event) {
  var imageWidth = image.offsetWidth;
  var clickPosition = event.clientX - image.getBoundingClientRect().left;

  if (clickPosition < imageWidth / 2) {
    prevView();
  } else if (clickPosition > imageWidth / 2){
    nextView();
  }
});

var valueList = document.getElementById('valueList');
valueList.addEventListener('change', function(event) {
    var selectedValue = event.target.value;
    location.href = '/catalog_manga/' + __manga_name + '/read?c=' + chapter + '&p=' + selectedValue;
});
var valueList = document.getElementById('btnPref');
valueList.addEventListener('click', function(event) {
    prevView();
});
var valueList = document.getElementById('btnNext');
valueList.addEventListener('click', function(event) {
    nextView();
});