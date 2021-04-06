// let switchMode = document.getElementById("switchMode")
//
// switchMode.onclick = function (){
//     let theme = document.getElementById("theme")
//     if (theme.getAttribute("href") === "../static/css/style-light.css") {
//         theme.href = "../static/css/style-dark.css"
//     }else {
//             theme.href = "../static/css/style-light.css"
//     }
//
// }


let hostUrl = window.location.pathname;
let options = 'fixed left 29%'
let main = document.getElementsByTagName('body')[0]
if(hostUrl === '/login' || hostUrl === '/register'){
    main.style.background = "#fff url(\"/static/images/Обои.jpg\") " + options;
}
if(hostUrl === '/'){
    main.style.background = "#fff url(\"/static/images/Обои.jpg\") " + options;
}
main.style.backgroundSize = 'auto 80%'