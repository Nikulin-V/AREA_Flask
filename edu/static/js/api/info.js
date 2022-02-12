/*
 * Nikulin Vasily © 2021
 */

info = Object()
info.subjects = function (fn = null) {
    if (fn)
        info.subjectsFn = fn
    else
        info.subjectsFn = null
    socket.emit('getSubjects')
}

socket.on('getSubjects', function (data) {
    info.subjectsJson = data
    if (info.subjectsFn)
        info.subjectsFn()
})

info.teachersList = function (fn = null) {
    if (fn)
        info.teachersListFn = fn
    else
        info.teachersListFn = null
    socket.emit('getTeachersList')
}

socket.on('getTeachersList', function (data) {
    info.teachersListJson = data
    if (info.teachersListFn)
        info.teachersListFn()
})