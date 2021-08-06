/*
 * Nikulin Vasily © 2021
 */

let sessions = Object()

sessions.get = function (title=null,
                     fn=null) {
    if (fn)
        sessions.getFn = fn
    else
        sessions.getFn = null
    socket.emit('getSessions')
}

socket.on('getSessions', function (data) {
    sessions.getJson = data
    if (sessions.getFn)
        sessions.getFn(data)
})


sessions.post = function (title=null,
                     fn=null) {
    if (fn)
        sessions.postFn = fn
    else
        sessions.postFn = null
    socket.emit('createSession', {
        'title': title
    })
}

socket.on('createSession', function (data) {
    sessions.postJson = data
    if (sessions.postFn)
        sessions.postFn(data)
})


sessions.put = function (
                        title=null,
                        adminsIds=null,
                        usersIds=null,
                        fn=null) {
    if (fn)
        sessions.putFn = fn
    else
        sessions.putFn = null
    socket.emit('editSession', {
        'title': title,
        'adminsIds': adminsIds,
        'playersIds': usersIds
    })
}

socket.on('editSession', function (data) {
    sessions.putJson = data
    if (sessions.putFn)
        sessions.putFn(data)
})


sessions.delete = function (fn=null) {
    if (fn)
        sessions.deleteFn = fn
    else
        sessions.deleteFn = null
    socket.emit('deleteSession')
}

socket.on('deleteSession', function (data) {
    sessions.deleteJson = data
    if (sessions.deleteFn)
        sessions.deleteFn(data)
})