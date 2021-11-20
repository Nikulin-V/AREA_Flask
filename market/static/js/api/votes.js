/*
 * Nikulin Vasily © 2021
 */

/*
 * Nikulin Vasily © 2021
 */

let votes = Object()

// Get current user votings
votes.get = function (fn=null) {
    if (fn)
        votes.getFn = fn
    else
        votes.getFn = null
    socket.emit('getCompaniesVotes')
}

socket.on('getCompaniesVotes', function (data) {
    votes.getJson = data
    if (votes.getFn)
        votes.getFn()
})

votes.put = function (companyTitle=null,
                      points=null,
                      fn=null) {
    if (fn)
        votes.putFn = fn
    else
        votes.putFn = null
    socket.emit('voteInCompaniesVoting', {
        'companyTitle': companyTitle,
        'points': points
    })
}

socket.on('voteInCompaniesVoting', function (data) {
    votes.putJson = data
    if (votes.putFn)
        votes.putFn(data)
})

// votes.get = function (fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/votes',
//         type: 'GET',
//         dataType: 'json',
//         success: function(data) {
//             votes.getJson = data
//             if (fn)
//                 fn()
//         }
//     })
// }
//
// votes.put = function (companyTitle, points, fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/votes?' +
//             'company=' + companyTitle + '&' +
//             'points=' + points,
//         type: 'PUT',
//         dataType: 'json',
//         success: function(data) {
//             votes.putJson = data
//             if (fn)
//                 fn(companyTitle, points, data)
//         }
//     })
// }
