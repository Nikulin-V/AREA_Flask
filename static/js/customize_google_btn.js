let googleUser = {};
let startApp = function () {
        gapi.load('auth2', function () {
            // Retrieve the singleton for the GoogleAuth library and set up the client.
            auth2 = gapi.auth2.init({
                client_id: '1031432130164-7eqo0g4hj6mht75nljoin36gs991lgjf.apps.googleusercontent.com',
            });
            googleAuth = gapi.auth2.getAuthInstance()
            console.log(googleAuth.isSignedIn.get())
            attachSignin(document.getElementById('customBtn'), googleAuth);
        });
    };

function attachSignin(element, googleAuth) {
    console.log(element.id);
    if (localStorage.getItem('googleUser') !== null) {
        let googleUser = googleAuth.currentUser.get()
        console.log(googleUser);
        document.getElementById('name').innerText = "Подключено";
        savingGoogleClassroomData(googleUser);
    }
    auth2.attachClickHandler(element, {},
        function(googleUser) {
            console.log(googleUser)
            console.log(googleUser.isSignedIn())
            document.getElementById('name').innerText = "Подключено"
            localStorage.setItem("googleUser", JSON.stringify(googleUser))
        }, function(error) {
            alert(JSON.stringify(error, undefined, 2));
        });
}
