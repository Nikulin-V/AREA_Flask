/*
 * Nikulin Vasily © 2021
 */

let news = Object()

news.get = function (page=0,
                     fn=null) {
    if (fn)
        news.getFn = fn
    else
        news.getFn = null
    socket.emit('getNews', {
        'page': page
    })
}

socket.on('getNews', function (data) {
    news.getJson = data
    if (news.getFn)
        news.getFn(data)
})


news.post = function (companyTitle=null,
                     title=null,
                     message=null,
                     imagePath=null,
                     jobId=null,
                     fn=null) {
    if (fn)
        news.postFn = fn
    else
        news.postFn = null
    socket.emit('createNews', {
        'companyTitle': companyTitle,
        'title': title,
        'message': message,
        'imagePath': imagePath,
        'jobId': jobId
    })
}

socket.on('createNews', function (data) {
    news.postJson = data
    if (news.postFn)
        news.postFn(data)
})


news.put = function (identifier=null,
                     title=null,
                     message=null,
                     imagePath=null,
                     isLike=null,
                     jobId=null,
                     fn=null) {
    if (fn)
        news.putFn = fn
    else
        news.putFn = null
    socket.emit('editNews', {
        'identifier': identifier,
        'title': title,
        'message': message,
        'imagePath': imagePath,
        'jobId': jobId,
        'isLike': isLike
    })
}

socket.on('editNews', function (data) {
    news.putJson = data
    if (news.putFn)
        news.putFn(data)
})


news.delete = function (identifier=null,
                        fn=null) {
    if (fn)
        news.deleteFn = fn
    else
        news.deleteFn = null
    socket.emit('deleteNews', {
        'identifier': identifier
    })
}

socket.on('deleteNews', function (data) {
    news.deleteJson = data
    if (news.deleteFn)
        news.deleteFn(data)
})

news.uploadImage = (image, progress = null, fn = null, fnTooLarge = null) => {
    let form = new FormData();
    form.append("illustration", image, image.name)

    $.ajax({
        url: imageUploadEndpoint,
        data: form,
        cache: false,
        contentType: false,
        processData: false,
        method: 'POST',
        xhr: () => {
            let xhr = $.ajaxSettings.xhr()
            xhr.upload.addEventListener('progress', e => {
                if(e.lengthComputable) {
                    const percent = Math.ceil(e.loaded / e.total * 100)

                    progress(percent)
                }
            }, false)
            return xhr
        },
        success: (data) => {
            fn(data)
        },
        statusCode: {
            413: fnTooLarge
        }
    })
}