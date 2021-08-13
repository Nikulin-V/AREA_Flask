/*
 * Nikulin Vasily © 2021
 */

socket.on('renderPage', function () {
    if (typeof renderPage !== 'undefined')
        renderPage()
})

socket.on('showNotifications', function (data) {
    for (i = 0; i < data['notifications'].length; i++) {
        n = Object(data['notifications'][i])
        showNotifications(n.logoSource, n.author, n.company, n.date, n.time, n.message, n.redirectLink)
    }
})