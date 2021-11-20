/*
 * Nikulin Vasily © 2021
 */

/*
 * Nikulin Vasily © 2021
 */

let svotes = Object()

// Get current user votings
svotes.get = function (fn=null) {
    if (fn)
        svotes.getFn = fn
    else
        svotes.getFn = null
    socket.emit('getStockholdersVotes')
}

socket.on('getStockholdersVotes', function (data) {
    svotes.getJson = data
    if (svotes.getFn)
        svotes.getFn(data)
})

svotes.put = function (votingId=null,
                       fn=null) {
    if (fn)
        svotes.putFn = fn
    else
        svotes.putFn = null
    socket.emit('voteInStockholdersVoting',{
        'identifier': votingId
    })
}

socket.on('voteInStockholdersVoting', function (data) {
    svotes.putJson = data
    if (svotes.putFn)
        svotes.putFn(data)
})


svotes.post = function (action=null,
                        companyTitle=null,
                        count=null,
                        fn=null) {
    if (fn)
        svotes.postFn = fn
    else
        svotes.postFn = null
    socket.emit('createStockholdersVoting',{
        'action': action,
        'companyTitle': companyTitle,
        'count': count
    })
}

socket.on('createStockholdersVoting', function (data) {
    svotes.postJson = data
    if (svotes.postFn)
        svotes.postFn()
})

// svotes.get = function (fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/svotes',
//         type: 'GET',
//         dataType: 'json',
//         success: function(data) {
//             svotes.getJson = data
//             if (fn)
//                 fn()
//         }
//     })
// }
//
// svotes.put = function (votingId, fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/svotes?' +
//             'identifier=' + votingId,
//         type: 'PUT',
//         dataType: 'json',
//         success: function(data) {
//             svotes.putJson = data
//             if (fn)
//                 fn(voting_id, data)
//         }
//     })
// }
//
// svotes.post = function (action=null, companyTitle=null, count=null, fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/svotes?' +
//             'companyTitle=' + companyTitle + '&' +
//             'action=' + action + '&' +
//             'count=' + count,
//         type: 'POST',
//         dataType: 'json',
//         success: function(data) {
//             svotes.postJson = data
//             if (fn)
//                 fn(data)
//         }
//     })
// }