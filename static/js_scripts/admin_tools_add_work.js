let genres = []
for (let i = 0; i < 16; i++){
    genres.push(0);
}

function getCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1, c.length);
        } if (c.indexOf(nameEQ) === 0) {
            return c.substring(nameEQ.length, c.length);
        }
    }
    return null;
}

fetch("/api/resources/all_work_genres").then(function(response) {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.text();
    }).then(function(data) {
        data = JSON.parse(data);
        if (data["status"] === "success") {
            let container = document.getElementById("input-genres-checkbox-list")
            for (var key in data["data"]) {
                let item = document.createElement("option");
                item.setAttribute("value", key);
                item.setAttribute("name", key);
                item.textContent = data["data"][key];
                container.appendChild(item);
            }
            const options = container.options;
            for (let i = 0; i < options.length; i++) {
                const option = options[i];
                const checkboxButton = document.createElement('div');
                checkboxButton.classList.add('input-genres-checkbox-button');
                checkboxButton.textContent = option.textContent;
                checkboxButton.value = option.value;
                checkboxButton.name = option.name;
                checkboxButton.addEventListener('click', function () {
                    option.selected = !option.selected;
                    if (option.selected) {
                        checkboxButton.classList.add('selected');
                        genres[option.value] = 1;
                    } else {
                        checkboxButton.classList.remove('selected');
                        genres[option.value] = 0;
                    }
                });
                if (option.selected) {
                    checkboxButton.classList.add('selected');
                }
                container.parentNode.insertBefore(checkboxButton, container.nextSibling);
            }
        }
    }).catch(function(error) {
        console.log("There was a problem with the fetch operation: ", error.message);
    });

document.getElementById("upload-new-work")
    .addEventListener("submit", function(event) {
        event.preventDefault();
        let formData = new FormData();
        formData.append("login", getCookie("user_login"));
        formData.append("password", getCookie("user_password"));
        let set_work_id = document.getElementById('set-work-id');
        formData.append('id', set_work_id.value);
        let set_work_name = document.getElementById('set-work-name');
        formData.append('ru_name', set_work_name.value);
        let set_work_desc = document.getElementById('set-work-desc');
        formData.append('desc', set_work_desc.value);
        let line_genre = "";
        for (let i = 0; i < genres.length; i++){
            line_genre = line_genre + genres[i];
        }
        formData.append('genre', line_genre);
        let fileInput = document.getElementById('pre_file_img');
        formData.append('pre_img', fileInput.files[0]);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/resources/add_work', true);
        xhr.onload = function () {
            let msg = document.getElementById("query-msg-add-work");
            if (xhr.status === 200) {
                msg.textContent = JSON.parse(xhr.response).message;
                msg.style.color = "red";
            } else {
                msg.textContent = "Произведение успешно загруженно на сайт.";
                msg.style.color = "black";
            }
        };
        xhr.send(formData);
    });
