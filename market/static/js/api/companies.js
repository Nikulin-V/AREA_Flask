/*
 * Nikulin Vasily © 2021
 */

/*
 * Nikulin Vasily © 2021
 */

let companies = Object()

// Get current session companies
companies.get = function (fn = null) {
    if (fn)
        companies.getFn = fn
    else
        companies.getFn = null
    socket.emit('getCompanies')
}

socket.on('getCompanies', function (data) {
    companies.getJson = data
    if (companies.getFn)
        companies.getFn()
})

companies.post = function (sector = null,
                           title = null,
                           description = null,
                           logoPath = null,
                           fn = null) {
    if (fn)
        companies.postFn = fn
    else
        companies.postFn = null
    socket.emit('createCompany', {
        'sector': sector,
        'title': title,
        'description': description,
        'logoPath': logoPath
    })
}

socket.on('createCompany', function (data) {
    companies.postJson = data
    if (companies.postFn)
        companies.postFn()
})

companies.delete = function (companyTitle = null,
                             fn = null) {
    if (fn)
        companies.deleteFn = fn
    else
        companies.deleteFn = null
    socket.emit('deleteCompany', {
        'companyId': null,
        'companyTitle': companyTitle
    })
}

socket.on('deleteCompany', function (data) {
    companies.deleteJson = data
    if (companies.deleteFn)
        companies.deleteFn()
})

// companies.get = function (fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/companies',
//         type: 'GET',
//         dataType: 'json',
//         success: function(data) {
//             companies.getJson = data
//             if (fn)
//                 fn(data)
//         }
//     })
// }
//
// companies.post = function (sector, title, description=null, logoUrl=null, fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/companies?' +
//             'sector=' + sector + '&' +
//             'title=' + title + '&' +
//             'description=' + description +'&' +
//             'logoUrl=' + logoUrl,
//         type: 'POST',
//         dataType: 'json',
//         success: function(data) {
//             companies.postJson = data
//             if (fn)
//                 fn()
//         }
//     })
// }
//
// companies.delete = function (companyTitle, fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/companies?' +
//             'companyTitle=' + companyTitle,
//         type: 'DELETE',
//         dataType: 'json',
//         success: function(data) {
//             companies.deleteJson = data
//             if (fn)
//                 fn()
//         }
//     })
// }

companies.uploadImage = (image, progress = null, fn = null, fnTooLarge = null) => {
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
                if (e.lengthComputable) {
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