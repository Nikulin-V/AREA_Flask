let googleUser = {};
let startApp = function () {
    gapi.load('auth2', function () {
        // Retrieve the singleton for the GoogleAuth library and set up the client.
        auth2 = gapi.auth2.init({
            client_id: '1031432130164-7eqo0g4hj6mht75nljoin36gs991lgjf.apps.googleusercontent.com',
            cookiepolicy: 'single_host_origin',
            // Request scopes in addition to 'profile' and 'email'
            //scope: 'additional_scope'
        });
        attachSignin(document.getElementById('customBtn'));
    });
};


function attachSignin(element) {
    if (googleUser !== {}) {
        console.log(element.id);
        console.log(googleUser)
        document.getElementById('name').innerText = "Подключено"
    }
    else {
        console.log(element.id);
        auth2.attachClickHandler(element, {},
            function(googleUser) {
                document.getElementById('name').innerText = "Подключено"
            }, function(error) {
                alert(JSON.stringify(error, undefined, 2));
            });
    }
}