let SCROLL_ID = 0;
const LIMIT_SCROLL = 30;
const table_name_ = "manga";
let template_form = "________________";
const manga_genres = [
        "Романтика", "Драма", "Комедия", "Фэнтези", "Приключения", "Повседневность", "Киберпанк", "Психологическое",
        "Космос", "Магия", "Фантастика", "Пост-апокалипсис", "Боевик", "Меха", "Сверхъестественное", "Детектив"
    ];


function addItemsToBD(scroll_num){
    fetch("/api/manga/get_catalog", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            limit: LIMIT_SCROLL,
            offset: scroll_num * LIMIT_SCROLL,
            template: template_form
        })}
    ).then(response => response.json()).then(data => {
        if (data["result"]){
            for (let i = 0; i < data["data_list"].length; i++){
                let url_manga_read = '/catalog_manga/' + data["data_list"][i]["manga_name"] + '/';
                let url_title_image = '/api/get_file?file_id=' + data["data_list"][i]["manga_title_image"];
                let item = '<div class="catalog-manga-content">';
                item += '<a href="' + url_manga_read;
                item += '" class="catalog-manga-content-a"> ' + data["data_list"][i]["rus_manga_name"] + ' </a>';
                item += '<div class="catalog-manga-body">';
                item += '<img src="' + url_title_image;
                item += '" alt="' + data["data_list"][i]["manga_name"] + '">';
                item += '<p> ' + data["data_list"][i]["manga_description"] + ' </p>'
                item += '</div></div>'
                document.getElementById("catalog-manga").innerHTML += item;
            }
        }
    }).catch(error => {
        console.log(error);
    });
}


function main() {
    // Create buttons for input manga genres
    let manga_genres_container = document.getElementById("filter-genre-container");
    for(let i = 0; i < manga_genres.length; i++){
        element_btn = "<div><input type='checkbox' id='btn_genre_" + i + "' name='genre_" + i + "' checked/>";
        element_btn += "<label htmlFor='btn_genre_" + i + "'>" + manga_genres[i] + "</label></div>";
        manga_genres_container.innerHTML += element_btn;
    }
    for(let i = 0; i < manga_genres.length; i++){
        let btn = document.getElementById("btn_genre_" + i);
        btn.checked = false;
        btn.value = i;
    }
    addItemsToBD(SCROLL_ID);
    SCROLL_ID += 1;
}


window.addEventListener('scroll', function() {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        addItemsToBD(SCROLL_ID);
        SCROLL_ID += 1;
    }
});


let button = document.getElementById("set-filters-button");
button.addEventListener("click", function (event){
    event.preventDefault();
    let temp = "";
    for (let i = 0; i < manga_genres.length; i++){
        let btn_ch = document.getElementById("btn_genre_" + i);
        if (btn_ch.checked){
            temp = temp + "1";
        }else{
            temp = temp + "_";
        }
    }
    template_form = temp;
    let catMan = document.getElementById("catalog-manga");
    catMan.innerHTML = '';
    SCROLL_ID = 0;
    addItemsToBD(SCROLL_ID);
    SCROLL_ID += 1;
})


main();