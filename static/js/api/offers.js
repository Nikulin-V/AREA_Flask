/*
 * Nikulin Vasily © 2021
 */

let offers = Object()

// Get current session offers
offers.get = function (fn=null) {
    if (fn)
        offers.getFn = fn
    else
        offers.getFn = null
    socket.emit('getOffers')
}

socket.on('getOffers', function (data) {
    offers.getJson = data
    if (offers.getFn)
        offers.getFn()
})

offers.post = function (company=null,
                        stocks=null,
                        price=null,
                        fn=null) {
    if (fn)
        offers.postFn = fn
    else
        offers.postFn = null
    socket.emit('createOffer',{
        'company': company,
        'stocks': stocks,
        'price': price
    })
}

socket.on('createOffer', function (data) {
    offers.postJson = data
    if (offers.postFn)
        offers.postFn()
})

offers.delete = function (company=null,
                        stocks=null,
                        price=null,
                        fn=null) {
    if (fn)
        offers.deleteFn = fn
    else
        offers.deleteFn = null
    socket.emit('deleteOffer',{
        'company': company,
        'stocks': stocks,
        'price': price
    })
}

socket.on('deleteOffer', function (data) {
    offers.deleteJson = data
    if (offers.deleteFn)
        offers.deleteFn()
})

offers.put = function (company=null,
                       stocks=null,
                       isBuy=null,
                       json=null,
                       fn=null) {
    if (fn)
        offers.putFn = fn
    else
        offers.putFn = null
    socket.emit('editOffer',{
        'company': company,
        'stocks': stocks,
        'isBuy': isBuy,
        'json': json
    })
}

socket.on('editOffer', function (data) {
    offers.putJson = data
    if (offers.putFn)
        offers.putFn()
})

// }// Get current session offers
// offers.get = function (fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/offers',
//         type: 'GET',
//         dataType: 'json',
//         success: function(data) {
//             offers.getJson = data
//             if (fn)
//                 fn(data)
//         }
//     })
// }
//
// offers.post = function (company, stocks, price, fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/offers?' +
//             'company=' + company + '&' +
//             'stocks=' + stocks + '&' +
//             'price=' + price,
//         type: 'POST',
//         dataType: 'json',
//         success: function(data) {
//             offers.postJson = data
//             if (fn)
//                 fn()
//         }
//     })
// }
//
// offers.delete = function (company, stocks, price, fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/offers?' +
//             'company=' + company + '&' +
//             'stocks=' + stocks + '&' +
//             'price=' + price,
//         type: 'DELETE',
//         dataType: 'json',
//         success: function(data) {
//             offers.deleteJson = data
//             if (fn)
//                 fn()
//         }
//     })
// }
//
// offers.put = function (company=null, stocks=null, isBuy=null,
//                        json=null,fn=null) {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/offers?' +
//             'company=' + company + '&' +
//             'stocks=' + stocks + '&' +
//             'isBuy=' + isBuy,
//         type: 'PUT',
//         contentType: 'application/json',
//         data: JSON.stringify(json),
//         success: function(data) {
//             offers.prevPutJson = offers.putJson
//             offers.putJson = data
//             if (fn)
//                 fn()
//         }
//     })
// }