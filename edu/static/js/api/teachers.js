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

teachers.post = function (surname = null,
                          name = null,
                          patronymic = null,
                          roles = ['user', 'teacher'],
                          fn = null) {
    if (fn)
        teachers.postFn = fn
    else
        teachers.postFn = null
    let email = translit(surname) + translit(name)[0].toUpperCase() + '@area-146.tk'
    let password = translit(surname) + translit(name)[0].toUpperCase() + '_password'
    socket.emit('createUser', {
        'email': email,
        'password': password,
        'surname': surname,
        'name': name,
        'patronymic': patronymic,
        'roles': roles,
        'school_id': 'current'
    })
}

socket.on('createUser', function (data) {
    teachers.postJson = data
    if (teachers.postFn)
        teachers.postFn(data)
})

teachers.put = function (surname = null,
                         name = null,
                         patronymic = null,
                         roles = ['user', 'teacher'],
                         fn = null) {
    if (fn)
        teachers.putFn = fn
    else
        teachers.putFn = null

    socket.emit('editTeacher', {
        'surname': surname,
        'name': name,
        'patronymic': patronymic,
        'roles': roles
    })
}

socket.on('editTeacher', function (data) {
    teachers.putJson = data
    if (teachers.putFn)
        teachers.putFn(data)
})

teachers.delete = function (surname = null,
                            name = null,
                            patronymic = null,
                            roles = null,
                            fn = null) {
    if (fn)
        teachers.deleteFn = fn
    else
        teachers.deleteFn = null

    socket.emit('deleteTeacher', {
        'surname': surname,
        'name': name,
        'patronymic': patronymic,
        'roles': roles
    })
}

socket.on('deleteTeacher', function (data) {
    teachers.deleteJson = data
    if (teachers.deleteFn)
        teachers.deleteFn(data)
})

function translit(word) {
    let answer = '';
    const converter = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ь': '', 'ы': 'y', 'ъ': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',

        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
        'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'C', 'Ч': 'Ch',
        'Ш': 'Sh', 'Щ': 'Sch', 'Ь': '', 'Ы': 'Y', 'Ъ': '',
        'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    };

    for (let i = 0; i < word.length; ++i) {
        if (converter[word[i]] === undefined) {
            answer += word[i];
        } else {
            answer += converter[word[i]];
        }
    }

    return answer;
}