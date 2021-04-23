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

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log(googleUser.getAuthPesponse())
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
}

// Homework spinner
let homework_link = document.getElementById('homework-link')
homework_link.onclick = function () {
    let homework_spinner = document.getElementById('homework-spinner')
    homework_spinner.style.visibility = "visible"
}

let myModal = document.getElementById('myModal');
let myInput = document.getElementById('myInput');

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})

let modal_close_btn = document.getElementById('modal-close-btn')
modal_close_btn.onclick = function () {
    $("#myModal").modal('hide');
}

let modal_ok_btn = document.getElementById('modal-ok-btn')
modal_ok_btn.onclick = function () {
    $("#myModal").modal('hide');
}