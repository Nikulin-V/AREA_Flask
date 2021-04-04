let
    switchMode = document.getElementById("switchMode")

switchMode.onclick = function (){
    let theme = document.getElementById("theme")
    if (theme.getAttribute("href") === "../static/css/style-light.css") {
        theme.href = "../static/css/style-dark.css"
    }else {
            theme.href = "../static/css/style-light.css"
    }

}