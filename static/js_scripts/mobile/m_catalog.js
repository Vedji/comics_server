let work_limit_on_page = 54;
let work_current_page = 0;
let current_template = "";
let current_search = "";
let last_element = undefined;
let count_works = 0;
let last_fetch_count_works = 0;

document.getElementById("header-menu-open").addEventListener("click", function (ev) {
    ev.preventDefault();
    document.getElementById("main-nav-menu").style.display = "block";
})
document.getElementById("btn-filter-genre").addEventListener("click", function (ev) {
    ev.preventDefault();
    document.getElementById("water-menu").style.display = 'block';
});
document.getElementById("water-menu-genres-header-close").addEventListener("click", function (ev) {
    ev.preventDefault();
    document.getElementById("water-menu").style.display = 'none';
});
document.getElementById("water-menu-genres-list-btn-reset").addEventListener("click", function (ev) {
    ev.preventDefault();
    setGenres();
    document.getElementById("filter-menu-search-input").value = "";
    work_current_page = 0;
    current_template = "";
    current_search = "";
    appendWorks(work_limit_on_page, work_current_page * work_limit_on_page, current_template, current_search);
    document.getElementById("water-menu").style.display = 'none';
});
document.getElementById("water-menu-genres-list-btn-show").addEventListener("click", function (ev) {
    ev.preventDefault();
    document.getElementById("filter-menu-search-input").value = "";
    let btn_genres = document.getElementsByClassName("genre-checkbox");
    let result_genre = Array(btn_genres.length).fill("_");
    for (let i = 0; i < btn_genres.length; i++){
        if (!btn_genres.item(i).hasAttribute("data-checked") || !btn_genres.item(i).hasAttribute("data-genre"))
            continue;
        let checked = btn_genres.item(i).getAttribute("data-checked");
        let genre_index = Number(btn_genres.item(i).getAttribute("data-genre"));
        if (checked === "0")
            continue;
        result_genre[genre_index] = "1";
    }
    work_current_page = 0;
    current_template = result_genre.join("");
    current_search = "";
    appendWorks(work_limit_on_page, work_current_page * work_limit_on_page, current_template, current_search);
    document.getElementById("water-menu").style.display = 'none';
})

document.getElementById("filter-menu-search-button").addEventListener("click", function (ev) {
    ev.preventDefault();
    let input_search = document.getElementById("filter-menu-search-input").value;
    if (input_search.length === 0 && current_search.length !== 0){
        appendWorks()
        setGenres();
        work_current_page = 0;
        current_template = "";
        current_search = "";
        appendWorks(work_limit_on_page, work_current_page * work_limit_on_page, current_template, current_search);
        return;
    }
    if (input_search === current_search)
        return;
    setGenres();
    work_current_page = 0;
    current_template = "";
    current_search =  input_search;
    appendWorks(work_limit_on_page, work_current_page * work_limit_on_page, current_template, current_search);
});

function setGenres() {
    let genres_container = document.getElementById("water-menu-genres-list");
    genres_container.innerHTML = "";
    fetch('/api/resources/all_work_genres').then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        if (data["status"] === "success"){
            if (data["data"].length === 0){
                alert("No images");
            }
            for (let i in data["data"]){
                let btn = document.createElement("button");
                btn.setAttribute("class", "genre-checkbox water-menu-genres-list-btn-unchecked");
                btn.setAttribute("data-checked", "0");
                btn.setAttribute("data-genre", i);
                btn.textContent = data["data"][i];
                btn.addEventListener("click", function (ev) {
                    ev.preventDefault();
                    if (!this.hasAttribute("data-checked") || !this.hasAttribute("data-genre")){
                        alert("Reload page: Error in genres");
                        return;
                    }
                    if (this.getAttribute("data-checked") === "0") {
                        this.setAttribute("class", "genre-checkbox water-menu-genres-list-btn-checked");
                        this.setAttribute("data-checked", "1")
                    }
                    else {
                        this.setAttribute("class", "genre-checkbox water-menu-genres-list-btn-unchecked");
                        this.setAttribute("data-checked", "0")
                    }
                });
                genres_container.appendChild(btn);
            }
        }
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function appendWorks(limit = -1, offset = 0, temp = "", search = "") {
    let params = {
        limit: limit,
        offset: offset,
        genre: temp,
        search_name: search
    }
    let urlWithParams = `/api/v1/work?${(new URLSearchParams(params)).toString()}`;
    let work_container = document.getElementById("work-container");
    if (offset === 0){
        work_container.innerHTML = "";
        count_works = 0;
        last_fetch_count_works = work_limit_on_page;
        last_element = undefined;
    }
    if (last_fetch_count_works < work_limit_on_page)
        return;

    fetch(urlWithParams).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {

        if (data["status"] === "success"){
            last_fetch_count_works = data["data"]["catalog"].length;
            count_works += data["data"]["catalog"].length;
            if (data["data"]["catalog"].length === 0){
                if (count_works > 0)
                    return;
                last_element = undefined;
                let p = document.createElement("p");
                p.textContent = "Ничего не найдено";
                p.setAttribute("class", "text_work_not_found");
                work_container.appendChild(p);
                return;
            }
            for (let i = 0; i < data["data"]["catalog"].length; i++) {
                let url_manga_read = '/catalog_manga/' + data["data"]["catalog"][i]["id"] + '/';
                let url_title_image = '/api/get_file?file_id=' + data["data"]["catalog"][i]["pre_img"];
                let a = document.createElement("a");
                a.setAttribute("href", url_manga_read);
                a.setAttribute("class", "work-container-item");
                let img = document.createElement("img");
                img.setAttribute("src", url_title_image);
                img.setAttribute("alt", data["data"]["catalog"][i]["id"]);
                a.appendChild(img);
                let p = document.createElement("p");
                p.textContent = data["data"]["catalog"][i]["ru_name"].toString();
                a.appendChild(p);
                last_element = a;
                work_container.appendChild(a);
            }
        }
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
window.addEventListener('scroll', function() {
    if (last_element === undefined && count_works > 0)
        return;
    if (last_element === undefined || last_fetch_count_works < work_limit_on_page)
        return;
    let rect = last_element.getBoundingClientRect();
    if (rect.top >= 0 && rect.bottom <= window.innerHeight){
        work_current_page += 1;
        appendWorks(work_limit_on_page, work_current_page * work_limit_on_page, current_template, current_search);
    }
});
appendWorks(work_limit_on_page, work_current_page * work_limit_on_page, current_template, current_search);
setGenres();