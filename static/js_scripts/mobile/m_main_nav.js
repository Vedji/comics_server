function getCookie(name, _default) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1, c.length);
        }
        if (c.indexOf(nameEQ) === 0) {
            return c.substring(nameEQ.length, c.length);
        }
    }
    return _default;
}

let ACCESS_TOKEN = getCookie("access_token", "");
let USER_ID = getCookie("user_id", "");
let USERNAME  = getCookie("username", "");
let USER_ROLE = Number(getCookie("user_role", 0));
function set_user_info(){
    let username = document.getElementById("main-nav-menu-username");
    let personal_account = document.getElementById("main-nav-menu-person-account");
    let headers = new Headers();
    headers.append('Authorization', `Bearer ${ACCESS_TOKEN}`)
    fetch("/api/v1/user", { method: 'GET', headers: headers }).then(response => {
        if (response.status === 401 || response.status === 422){
            username.textContent = "";
            username.style.visibility = "hidden";
            username.setAttribute("href", `/login`)
            personal_account.setAttribute("href", "/login");
            return response;
        }
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        if (data.hasOwnProperty("status") && data["status"] === "success") {
            username.textContent = data["data"]["USERNAME"]
            username.style.visibility = "visible";
            USER_ID = data["data"]["ID"];
            USERNAME = data["data"]["USERNAME"];
            USER_ROLE = data["data"]["ROLE"];
            username.setAttribute("href", `/user/${data["data"]["USERNAME"]}`)
            personal_account.setAttribute("href", `/user/${data["data"]["USERNAME"]}`);
        }
    }).catch((error) => {
        console.log(error);
        console.error('Error:', error);
    });
}

document.getElementById("header-menu-open").addEventListener("click", function (ev) {
    ev.preventDefault();
    document.getElementById("main-nav-menu").setAttribute("class", "open_nav_menu");
    document.getElementById("main-content-container").style.display = "none";
});
document.getElementById("main-nav-menu-close").addEventListener("click", function (ev) {
    ev.preventDefault();
    document.getElementById("main-nav-menu").setAttribute("class", "close_nav_menu");
    document.getElementById("main-content-container").style.display = "block";
})

set_user_info()