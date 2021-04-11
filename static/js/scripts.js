let hostUrl = window.location.pathname;
let options = 'fixed left 29%'
let main = document.getElementsByTagName('body')[0]
if(hostUrl === '/login' || hostUrl === '/register'){
    main.style.background = "#fff url(\"/static/images/.jpg\") " + options;
}
if(hostUrl === '/'){
    main.style.background = "#fff url(\"/static/images/.jpg\") " + options;
}
main.style.backgroundSize = 'auto 80%'

alert(document.cookie)
