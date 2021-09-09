/*
 * Nikulin Vasily © 2021
 */

teachers = Object()
teachers.get = function (fn = null) {
    if (fn)
        teachers.getFn = fn
    else
        teachers.getFn = null
    socket.emit('getTeachers')
}

socket.on('getTeachers', function (data) {
    teachers.getJson = data
    if (teachers.getFn)
        teachers.getFn()
})