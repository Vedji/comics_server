let pages_count = 0;
let pages_img_list = [];

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
function update(){
    let inp = document.getElementsByTagName("input");
    for (let i = 0; i < inp.length; i++){
        if (inp[i].id && inp[i].id.substring("inp-page-")){
            inp[i].addEventListener('change', function () {
                inp[i].style.background = "green";
            })
        }
    }
}
function btn_add_page_container(_page_number) {
    let container = document.getElementById("chapters-pages-container");

    let root = document.createElement("div");
    root.setAttribute("id", `chapter-num-container-${_page_number.toString()}`)
    root.setAttribute("class", "input-element input-chapter-file-content");
    let page_number = document.createElement("p");
    page_number.setAttribute("class", "field-header");
    page_number.textContent = `Страница ${(_page_number + 1).toString()}`
    page_number.setAttribute("id", `chapter-num-container-text-${_page_number.toString()}`)
    root.appendChild(page_number);
    let input_image_field = document.createElement("div");
    input_image_field.setAttribute("class", "input-element input-field");
        let page_img_p = document.createElement("p");
        page_img_p.setAttribute("class", "field-header");
        page_img_p.textContent = "Изображение страницы";
        input_image_field.appendChild(page_img_p);
        let inp_img = document.createElement("input");
        inp_img.setAttribute("class", "input-text-line");
        inp_img.setAttribute("type", "file");
        inp_img.setAttribute("name", `${_page_number.toString()}`)
        inp_img.setAttribute("id", `inp-page-${_page_number.toString()}`)
        input_image_field.appendChild(inp_img);
    root.appendChild(input_image_field);
    let btn_del = document.createElement("button");
    btn_del.setAttribute("type", "button");
    btn_del.setAttribute("class", "button-element button-del-chapter");
    btn_del.setAttribute("onclick", `btn_remove_img(${_page_number})`)
    btn_del.setAttribute("id", `btn-remove-work-from-chapter-${_page_number.toString()}`)
    btn_del.textContent = "Удалить";
    root.appendChild(btn_del);
    container.appendChild(root);
    update()
}

function btn_remove_img(img_number_removed) {
    pages_count -= 1;
    let container = document.getElementById("chapters-pages-container");
    if (pages_count < 0){
        pages_count = 0;
        return;
    }
    if (pages_count === 0){
        let item = document.getElementById(`chapter-num-container-${(0).toString()}`)
        container.innerHTML = "";
        return;
    }
    if (pages_count + 1 === img_number_removed){
        let item = document.getElementById(`chapter-num-container-${(pages_count + 1).toString()}`)
        container.removeChild(item);
        return;
    }

    container.removeChild(document.getElementById(`chapter-num-container-${img_number_removed.toString()}`));
    for (let i = img_number_removed; i < pages_count; i++){
        let item = document.getElementById(`chapter-num-container-${(i + 1).toString()}`)
        item.setAttribute("id", `chapter-num-container-${(i).toString()}`);
        let p = document.getElementById(`chapter-num-container-text-${i + 1}`);
        p.setAttribute("id",`chapter-num-container-text-${i}`)
        p.textContent = `Страница ${i+1}`;
        let edit = document.getElementById(`inp-page-${i + 1}`);
        edit.setAttribute("name", `${i.toString()}`);
        edit.setAttribute("id", `inp-page-${i.toString()}`);
        let btn = document.getElementById(`btn-remove-work-from-chapter-${i + 1}`);
        btn.setAttribute("id", `btn-remove-work-from-chapter-${i.toString()}`);
    }
    update()
}

document.getElementById("btn-add-chapter-to-container")
    .addEventListener("click", function (event) {
        event.preventDefault();
        btn_add_page_container(pages_count);
        pages_count += 1;
});

document.getElementById("upload-new-work-chapter")
    .addEventListener("submit", function(event) {
        event.preventDefault();

        let formData = new FormData();
        formData.append("login", getCookie("user_login"));
        formData.append("password", getCookie("user_password"));
        formData.append("id", document.getElementById("add-work-chapter").value);
        formData.append("chapter_name", document.getElementById("add-work-chapter-name").value);
        formData.append("chapter_num", document.getElementById("add-work-chapter-num").value);
        formData.append("count_files", pages_count);
        for (let i = 0; i < pages_count; i++ ){
            formData.append(`file_${i}`, document.getElementById(`inp-page-${i}`).files[0])
        }
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/resources/add_work_chapter', true);
        xhr.onload = function () {
            let msg = document.getElementById("query-msg-add-work-chapter");
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