/*
 * Nikulin Vasily © 2021
 */

workload = Object()
workload.get = function (classNumber = null,
                         classLetter = null,
                         fn = null) {
    if (fn)
        workload.getFn = fn
    else
        workload.getFn = null
    socket.emit('getWorkload', {
        'classNumber': classNumber,
        'classLetter': classLetter
    })
}

socket.on('getWorkload', function (data) {
    workload.getJson = data
    if (workload.getFn)
        workload.getFn()
})

workload.post = function (classNumber = null,
                          classLetter = null,
                          teacher = null,
                          title = null,
                          hours = 0,
                          groupNumber = 0,
                          fn = null) {
    if (fn)
        workload.postFn = fn
    else
        workload.postFn = null
    socket.emit('createWorkload', {
        'classNumber': classNumber,
        'classLetter': classLetter,
        'teacher': teacher,
        'title': title,
        'hours': hours,
        'groupNumber': groupNumber
    })
}

socket.on('createWorkload', function (data) {
    workload.postJson = data
    if (workload.postFn)
        workload.postFn(data)
})

workload.put = function (
    classNumber = null,
    classLetter = null,
    oldTeacher = null,
    oldTitle = null,
    oldHours = 0,
    oldGroupNumber = 0,
    teacher = null,
    title = null,
    hours = 0,
    groupNumber = 0,
    fn = null) {
    if (fn)
        workload.putFn = fn
    else
        workload.putFn = null
    socket.emit('editWorkload', {
        'classNumber': classNumber,
        'classLetter': classLetter,
        'oldTeacher': oldTeacher,
        'oldTitle': oldTitle,
        'oldHours': oldHours,
        'oldGroupNumber': oldGroupNumber,
        'teacher': teacher,
        'title': title,
        'hours': hours,
        'groupNumber': groupNumber
    })
}

socket.on('editWorkload', function (data) {
    workload.putJson = data
    if (workload.putFn)
        workload.putFn(data)
})

workload.delete = function (classNumber = null,
                            classLetter = null,
                            teacher = null,
                            title = null,
                            hours = 0,
                            groupNumber = 0,
                            fn = null) {
    if (fn)
        workload.deleteFn = fn
    else
        workload.deleteFn = null

    socket.emit('deleteWorkload', {
        'classNumber': classNumber,
        'classLetter': classLetter,
        'teacher': teacher,
        'title': title,
        'hours': hours,
        'groupNumber': groupNumber
    })
}

socket.on('deleteWorkload', function (data) {
    workload.deleteJson = data
    if (workload.deleteFn)
        workload.deleteFn(data)
})
