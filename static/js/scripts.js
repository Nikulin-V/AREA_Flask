let dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
dropdownElementList.map(function (dropdownToggleEl) {
    return new bootstrap.Dropdown(dropdownToggleEl)
});

let main = document.getElementsByTagName('body')[0]
let pageUrl = document.location.pathname
if (pageUrl === "/" || pageUrl === "/index") {
    main.style.backgroundImage = "url('/static/images/index-background.jpg')"
}


// Homework spinner
let homework_link = document.getElementById('epos-diary')
homework_link.onclick = function () {
    let homework_spinner = document.getElementById('epos-spinner')
    homework_spinner.style.visibility = "visible"
}

let myModal = document.getElementById('myModal');
let myInput = document.getElementById('myInput');

if (myModal && myInput) {
    myModal.addEventListener('shown.bs.modal', function () {
        myInput.focus()
})
}

let modal_close_btn = document.getElementById('modal-close-btn')
if (modal_close_btn) {
    modal_close_btn.onclick = function () {
        $("#myModal").modal('hide');
    }
}

let modal_ok_btn = document.getElementById('modal-ok-btn')
if (modal_ok_btn) {
    modal_ok_btn.onclick = function () {
        $("#myModal").modal('hide');
    }
}