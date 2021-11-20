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
    })
}

socket.on('createClass', function (data) {
    classes.postJson = data
    if (classes.postFn)
        classes.postFn(data)
})

classes.put = function (old_number = null,
                        old_letter = null,
                        number = null,
                        letter = null,
                        fn = null) {
    if (fn)
        classes.putFn = fn
    else
        classes.putFn = null

    socket.emit('editClass', {
        'old_number': old_number,
        'old_letter': old_letter,
        'number': number,
        'letter': letter,
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
        classes.putFn = fn
    else
        classes.putFn = null

    socket.emit('deleteClass', {
        'number': number,
        'letter': letter,
    })
}

socket.on('deleteClass', function (data) {
    classes.putJson = data
    if (classes.putFn)
        classes.putFn(data)
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