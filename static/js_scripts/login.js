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
        let name = document.getElementById("username").value;
        let pwd = document.getElementById("password").value;
        let data = {
            username: name,
            password: pwd
        };
        fetch("/api/v1/user/login", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).then(response => response.json()).then(data => {
            if (data["status"] === "success"){
                setCookie("access_token", data["data"]["access_token"], 7);
                console.log("access_token ", data);
                location.href = "/";
            }
        }).catch(error => {
            alert(error);
        });
    });