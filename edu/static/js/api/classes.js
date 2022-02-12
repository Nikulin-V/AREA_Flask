/*
 * Nikulin Vasily © 2021
 */

classes = Object()
classes.get = function (fn = null) {
    if (fn)
        classes.getFn = fn
    else
        classes.getFn = null
    socket.emit('getClasses')
}

socket.on('getClasses', function (data) {
    classes.getJson = data
    if (classes.getFn)
        classes.getFn()
})

classes.post = function (number = null,
                         letter = null,
                         fn = null) {
    if (fn)
        classes.postFn = fn
    else
        classes.postFn = null

    socket.emit('createClass', {
        'number': number,
        'letter': letter,
        'teacher': teacher
    })
}

socket.on('createClass', function (data) {
    classes.postJson = data
    if (classes.postFn)
        classes.postFn(data)
})

classes.put = function (old_number = null,
                        old_letter = null,
                        old_teacher = null,
                        number = null,
                        letter = null,
                        teacher = null,
                        fn = null) {
    if (fn)
        classes.putFn = fn
    else
        classes.putFn = null

    socket.emit('editClass', {
        'old_number': old_number,
        'old_letter': old_letter,
        'old_teacher': old_teacher,
        'number': number,
        'letter': letter,
        'teacher': teacher
    })
}

socket.on('editClass', function (data) {
    classes.putJson = data
    if (classes.putFn)
        classes.putFn(data)
})

classes.delete = function (number = null,
                           letter = null,
                           fn = null) {
    if (fn)
        classes.deleteFn = fn
    else
        classes.deleteFn = null

    socket.emit('deleteClass', {
        'number': number,
        'letter': letter,
        'teacher': teacher
    })
}

socket.on('deleteClass', function (data) {
    classes.deleteJson = data
    if (classes.deleteFn)
        classes.deleteFn(data)
})
