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
        showNotifications(n.logoSource, n.header_down, n.header_up, n.date, n.time, n.message, n.redirectLink)
    }
})

socket.on('connect', function () {
    socket.emit('registerUserSessionSID')
    if (typeof disconnected === 'boolean' && disconnected)
        showConnected()
    disconnected = false
})

socket.on('disconnect', function () {
    showConnected(false)
    disconnected = true
})