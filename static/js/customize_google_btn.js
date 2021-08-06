/*
 * Nikulin Vasily © 2021
 */

// noinspection JSUndeclaredVariable,JSUnresolvedFunction,JSUnresolvedVariable,JSUnusedLocalSymbols

let googleUser = {};
let startApp = function () {
        gapi.load('')
    gapi.load('auth2', function () {
            // Retrieve the singleton for the GoogleAuth library and set up the client.
            auth2 = gapi.auth2.init({
                client_id: '1031432130164-7eqo0g4hj6mht75nljoin36gs991lgjf.' +
                    'apps.googleusercontent.com',
            });
            googleAuth = gapi.auth2.getAuthInstance()
            attachSignin(document.getElementById('googleBtn'), googleAuth);
            if (localStorage.getItem("googleUser")){
                document.getElementById('name').innerText = "Подключено"
            }
        });
    };

function attachSignin(element, googleAuth) {
    let googleUser = googleAuth.currentUser.get()
    auth2.attachClickHandler(element, {},
        function(googleUser) {
            document.getElementById('name').innerText = "Подключено"
            onSignIn(googleUser)
            localStorage.setItem("googleUser", JSON.stringify(googleUser))
        }, function(error) {
            alert(JSON.stringify(error, undefined, 2));
        });
}
function onSignIn(googleUser) {
    let profile = googleUser.getBasicProfile();
    let id_token = googleUser.getAuthResponse().id_token;
    console.log(id_token)
    console.log(googleUser)
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail());
    localStorage.setItem("googleUser", JSON.stringify(googleUser))
    console.log(getCourse(profile.getId))
}