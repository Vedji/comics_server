var SCROLL_ID = 0;
var LIMIT_SCROLL = 30;
var table_name_ = "manga";
function addItemsToBD(scroll_num){
fetch("/api/bd/get_list", {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        table_name: table_name_,
        limit: LIMIT_SCROLL,
        offset: scroll_num * LIMIT_SCROLL
    })}
).then(response => response.json())
.then(data => {
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
    })
    .catch(error => {
        console.log(error);
    });
}
addItemsToBD(SCROLL_ID);
SCROLL_ID += 1;
window.addEventListener('scroll', function() {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
                addItemsToBD(SCROLL_ID);
                SCROLL_ID += 1;
            }
        });