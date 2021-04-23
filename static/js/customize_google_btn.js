let googleUser = {};
let startApp = function () {
        gapi.load('auth2', function () {
            // Retrieve the singleton for the GoogleAuth library and set up the client.
            auth2 = gapi.module.init({
                client_id: '1031432130164-7eqo0g4hj6mht75nljoin36gs991lgjf.apps.googleusercontent.com',
            });
            googleAuth = gapi.auth2.getAuthInstance()
            savingGoogleClassroomData(googleUser);
            attachSignin(document.getElementById('customBtn'), googleAuth);
        });
    };

function attachSignin(element, googleAuth) {
    let googleUser = googleAuth.currentUser.get()
    auth2.attachClickHandler(element, {},
        function(googleUser) {
            document.getElementById('name').innerText = "Подключено"
            localStorage.setItem("googleUser", JSON.stringify(googleUser))
        }, function(error) {
            alert(JSON.stringify(error, undefined, 2));
        });
}

function savingGoogleClassroomData(googleUser) {
      console.log(googleUser)
}
