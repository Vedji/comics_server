function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}
document.getElementById("loginForm")
    .addEventListener("submit", function(event) {
        event.preventDefault(); // Отменяем стандартное поведение формы
        // Получаем значения полей логина и пароля
        var username = document.getElementById("username").value;
        var password = document.getElementById("password").value;
        var data = {
            user_login: username,
            user_password: password
        };
        fetch("/api/user/user_info", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).then(response => response.json()).then(data => {
            if (data["result"]){
                setCookie("user_login", username, 7);
                setCookie("user_password", password, 7);
                location.href = "/user/" + username + "/";
            }
        }).catch(error => {
            alert(error);
        });
    });