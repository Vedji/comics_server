var SCROLL_ID = 0;
var LIMIT_SCROLL = 30;
var table_name_ = window.location.pathname.split('/')[2];
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
            console.log(data["data_list"][0]["manga_name"] + ", ");
            for (var i = 0; i < data["data_list"].length; i++){
                var html_form = "";
                var newRow = document.createElement("tr");
                for (var y = 0; y < data["header_list"].length; y++){
                    html_form +=  "<td>" + data["data_list"][i][data["header_list"][y]];
                    }
                newRow.innerHTML = html_form;
                document.getElementById("dataTable").getElementsByTagName("tbody")[0].appendChild(newRow);
            }
        }
    })
    .catch(error => {

    });
}
addItemsToBD(SCROLL_ID);
SCROLL_ID += 1;
document.getElementById("addButton").addEventListener("click", function() {
    document.getElementById("popupForm").classList.remove("hidden");
    });


document.getElementById("addButton").addEventListener("click", function() {
            document.getElementById("popupForm").classList.remove("hidden");
        });

window.addEventListener('scroll', function() {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
                addItemsToBD(SCROLL_ID);
                SCROLL_ID += 1;
            }
        });