let SCROLL_ID = 0;
const LIMIT_SCROLL = 30;
const table_name_ = "manga";
let template_form = "________________";
const manga_genres = [
        "Романтика", "Драма", "Комедия", "Фэнтези", "Приключения", "Повседневность", "Киберпанк", "Психологическое",
        "Космос", "Магия", "Фантастика", "Пост-апокалипсис", "Боевик", "Меха", "Сверхъестественное", "Детектив"
    ];


function addToSearchMenu(query_line) {
    let url = '/api/v1/work';
    var line = query_line.toString();
    if (line){
        line = line.replace(" ", "+");
    }
    let params = {
        limit: 10,
        offset: 0,
        search_name: line
    };
    let paramToURL = new URLSearchParams(params).toString();
    let urlWithParams = `${url}?${paramToURL}`;
    fetch(urlWithParams).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        let catalog_works_search_output = document.getElementById("catalog-works-search-output");
        catalog_works_search_output.innerHTML = "";
        if (data["status"] === "success"){
            if (data["data"]["catalog"].length === 0){
                let work_container = document.createElement("div");
                work_container.setAttribute("class", "search-result-catalog")
                let work_name = document.createElement("p");
                work_name.textContent = "Ничего не найдено! увы(";
                work_container.appendChild(work_name);
                catalog_works_search_output.appendChild(work_container);
            }
            for (let i = 0; i < data["data"]["catalog"].length; i++) {
                let url_manga_read = '/catalog_manga/' + data["data"]["catalog"][i]["id"] + '/';
                let url_title_image = '/api/get_file?file_id=' + data["data"]["catalog"][i]["pre_img"];

                let work_container = document.createElement("div");
                work_container.setAttribute("class", "search-result-catalog")
                let work_pre_img = document.createElement("img");
                work_pre_img.setAttribute("src", url_title_image);
                work_pre_img.setAttribute("alt", data["data"]["catalog"][i]["ru_name"]);
                let work_name = document.createElement("a");
                work_name.setAttribute("href", url_manga_read);
                work_name.textContent = data["data"]["catalog"][i]["ru_name"];
                work_container.appendChild(work_pre_img);
                work_container.appendChild(work_name);
                catalog_works_search_output.appendChild(work_container);
            }
        }
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function addWorksToList(scroll_num){
    let url = '/api/v1/work';
    let params = {
        limit: LIMIT_SCROLL.toString(),
        offset: (scroll_num * LIMIT_SCROLL).toString(),
        genre: template_form
    };
    let paramToURL = new URLSearchParams(params).toString();
    let urlWithParams = `${url}?${paramToURL}`;
    console.log(urlWithParams);
    fetch(urlWithParams).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        if (data["status"] === "success"){
            console.log(data["data"]["catalog"]);
            for (let i = 0; i < data["data"]["catalog"].length; i++) {
                let url_manga_read = '/catalog_manga/' + data["data"]["catalog"][i]["id"] + '/';
                let url_title_image = '/api/get_file?file_id=' + data["data"]["catalog"][i]["pre_img"];
                let work_container = document.createElement("div");
                work_container.setAttribute("class", "catalog-manga-content")
                let work_name = document.createElement("a");
                work_name.setAttribute("href", url_manga_read);
                work_name.setAttribute("class", "catalog-manga-content-a");
                work_name.textContent = data["data"]["catalog"][i]["ru_name"];
                work_container.appendChild(work_name);
                let work_body_container = document.createElement("div");
                work_body_container.setAttribute("class", "catalog-manga-body")
                let work_pre_img = document.createElement("img");
                work_pre_img.setAttribute("src", url_title_image);
                work_pre_img.setAttribute("alt", data["data"]["catalog"][i]["ru_name"]);
                work_body_container.appendChild(work_pre_img);
                let word_desc = document.createElement("p");
                word_desc.textContent = data["data"]["catalog"][i]["desc"];
                work_body_container.appendChild(word_desc);
                work_container.appendChild(work_body_container);
                document.getElementById("catalog-manga").appendChild(work_container);
            }
        }
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}


function main() {
    // Create buttons for input manga genres
    let works_genres_container = document.getElementById("filter-genre-container");
    for(let i = 0; i < manga_genres.length; i++){
        let btn_container = document.createElement("div");
        btn_container.setAttribute("class", "filter-genre-element")
        let btn = document.createElement("input");
        btn.setAttribute("type", "checkbox");
        btn.setAttribute("id", `btn_genre_${i}`);
        btn.setAttribute("value", i.toString());
        btn_container.appendChild(btn);
        let btn_label = document.createElement("label");
        btn_label.setAttribute("htmlFor", `btn_genre_${i}`);
        btn_label.textContent = `${manga_genres[i]}`;
        btn_container.appendChild(btn_label);
        works_genres_container.appendChild(btn_container);
    }
    addWorksToList(SCROLL_ID);
    SCROLL_ID += 1;
}


window.addEventListener('scroll', function() {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        addWorksToList(SCROLL_ID);
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
    let catMan = document.getElementById("catalog-manga").innerHTML = '';
    addWorksToList(0);
    SCROLL_ID = 1;
})

let searchBtnShow = document.getElementById("search-button");
searchBtnShow.addEventListener("click", function (){
    let searchMenu = document.getElementById("catalog-works-search");
    searchMenu.style.display = "block";
})

let searchBtnClose = document.getElementById("catalog-works-search-close");
searchBtnClose.addEventListener("click", function (){
    let searchMenu = document.getElementById("catalog-works-search");
    searchMenu.style.display = "none";
})

let searchInput = document.getElementById("searchInput");
searchInput.addEventListener("input", function () {
    if (this.value.length > 2){
        addToSearchMenu(this.value);
    }
})

main();