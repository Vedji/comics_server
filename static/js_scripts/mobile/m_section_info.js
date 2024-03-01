const first_init_layout = "section-comments";
try { user_role = USER_ROLE; }catch (error){ console.log("USER_ROLE's not initialization"); }
try { access_token = ACCESS_TOKEN; }catch (error){ console.log("user not initialization, not ACCESS_TOKEN"); }
try { username = USERNAME; }catch (error){ console.log("user not authorization, not AUTHORIZATION"); }
let _sections = document.getElementsByClassName("pag-nav-item");
let nav_menu = {
    "section-info": {
        "layouts": [document.getElementById("section-description-layout")]
    },
    "section-chapters": {
        "layouts": [document.getElementById("section-chapters-layout")]
    },
    "section-comments": {
        "layouts": [document.getElementById("section-comments-layout")]
    }
}
function section_navigation(section) {
    for (let nav in nav_menu){
        for (let y = 0; y < nav_menu[nav]["layouts"].length; y++){
            if (nav === section){
                nav_menu[nav]["layouts"][y].style.display = "block";
            }else{
                nav_menu[nav]["layouts"][y].style.display = "none";
            }
        }
    }
}


for (let i = 0; i < _sections.length; i++){
    if (!_sections.item(i).hasAttribute("data-section"))
        continue;
    _sections.item(i).addEventListener("click", function (ev) {
        ev.preventDefault();
        section_navigation(_sections.item(i).getAttribute("data-section"));
        let bottom_line = document.getElementById("page-nav-line");
        let rect = _sections.item(i).getBoundingClientRect();
        bottom_line.style.left = `${rect.left}px`;
        bottom_line.style.bottom = `${rect.bottom}px`;
        bottom_line.style.width = `${rect.width}px`;
        bottom_line.style.top = `${rect.height}px`;
    })
    if (_sections.item(i).getAttribute("data-section") === first_init_layout)
        _sections.item(i).click();
}
section_navigation(first_init_layout);