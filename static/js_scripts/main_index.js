function getCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1, c.length);
    }
    if (c.indexOf(nameEQ) === 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
}

var data = {
    user_login: getCookie("user_login"),
    user_password: getCookie("user_password")
};
fetch("/api/user/user_info", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
}).then(response => response.json())
.then(data => {
var username = document.getElementById("user_login");
  if (data["result"]){
    username.text = data["user_name"];
    username.href = "/user/" + data["user_name"] + "/";
  }else{
    username.href = "/login";
  }
})
.catch(error => {
  alert(error);
});