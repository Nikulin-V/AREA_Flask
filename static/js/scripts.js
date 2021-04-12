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

let dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
let dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
    return new bootstrap.Dropdown(dropdownToggleEl)
});