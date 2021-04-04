let
    switchMode = document.getElementById("switchMode")

switchMode.onclick = function (){
    let theme = document.getElementById("theme")
    if (theme.getAttribute("href") === "../css/style-light.css") {
        theme.href = "../css/style-dark.css";
    }else {
            theme.href = "../css/style-light.css";
    }

}