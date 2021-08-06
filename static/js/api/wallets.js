/*
 * Nikulin Vasily © 2021
 */

/*
 * Nikulin Vasily © 2021
 */

let wallet = Object()

wallet.get = function (fn=null) {
    if (fn)
        wallet.getFn = fn
    else
        wallet.getFn = null
    socket.emit('getWalletMoney')
}

socket.on('getWalletMoney', function (data) {
    wallet.money = parseInt(data['money'])
    if (wallet.getFn)
        wallet.getFn()
})

// wallet.get = function () {
//     $.ajax({
//         url: 'http://market.area-146.ru/api/wallets',
//         type: 'GET',
//         dataType: 'json',
//         success: function (data) {
//             wallet.money = data['money']
//         }
//     })
// }
