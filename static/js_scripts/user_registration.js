function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

document.getElementById("loginForm")
    .addEventListener("submit", function(event) {
        event.preventDefault();
        let data = {
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        };
        fetch("/api/v1/user/registration", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).then(response => {
            return response.json()
        }).then(data => {
            console.log(data)
            if (data["status"] === "success"){
                setCookie("access_token", data["data"]["access_token"], 7);
                setCookie("user_id", data["data"]["ID"]);
                setCookie("username", data["data"]["USERNAME"]);
                setCookie("user_role", data["data"]["USER_ROLE"]);
                location.href = "/";
                location.href = "/user/" + username + "/";
            }else if (data["status"] === "error"){

                alert(data["message"]);
            }
        }).catch(error => {
            alert(error);
        });
    });