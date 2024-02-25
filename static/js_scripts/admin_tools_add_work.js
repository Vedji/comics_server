let genres = []
for (let i = 0; i < 16; i++){
    genres.push(0);
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
        let set_work_id = document.getElementById('set-work-id');
        formData.append('work_id', set_work_id.value);
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
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/v1/work', true);
        xhr.setRequestHeader("Authorization", `Bearer ${access_token}`);
        xhr.onload = function () {
            let msg = document.getElementById("query-msg-add-work");
            if (xhr.status === 200) {
                msg.textContent = "Глава успешно загруженна";
                msg.style.color = "green";
            }
            else if (xhr.status === 400 || xhr.status === 401){
                msg.textContent = JSON.parse(xhr.response).message;
                msg.style.color = "red";
            }
            else if (xhr.status === 422){
                msg.textContent = "Для таких действий нужно войти....";
                msg.style.color = "red";
            }
            else {
                msg.textContent = `Неизвестная ошибка со статусом ${xhr.status}`;
                msg.style.color = "red";
            }
        };
        xhr.send(formData);
    });
