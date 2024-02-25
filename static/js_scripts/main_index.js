function getCookie(name) {
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
    return null;
}
const access_token = getCookie("access_token");
const username = document.getElementById("user_login");

function set_user_info(){
    let headers = new Headers();
    headers.append('Authorization', `Bearer ${access_token}`)
    fetch("/api/v1/user", { method: 'GET', headers: headers }).then(response => {
        if (response.status === 401){
            username.textContent = "Войти";
            username.setAttribute("href", `/login`)
        }
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        if (data["status"] === "success") {
            console.log('Success:', data);
            username.textContent = data["data"]["USERNAME"]
            username.setAttribute("href", `/user/${data["data"]["USERNAME"]}`)
        }
    }).catch((error) => {
        console.error('Error:', error);
    });
}


set_user_info()