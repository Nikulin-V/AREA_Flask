/*
 * Nikulin Vasily © 2021
 */


let wallet = Object()

wallet.get = function (fn = null) {
    if (fn)
        wallet.getFn = fn
    else
        wallet.getFn = null
    socket.emit('getWalletMoney')
}

socket.on('getWalletMoney', function (data) {
    wallet.money = parseInt(data['money'])
    if (wallet.getFn)
        wallet.getFn(data)
})

wallet.getWallets = function (fn = null) {
    if (fn)
        wallet.getFn = fn
    else
        wallet.getFn = null
    socket.emit('getWallets')
}

socket.on('getWallets', function (data) {
    wallet.getJson = data
    if (wallet.getFn)
        wallet.getFn(data)
})


wallet.patch = function (walletId, money, fn = null) {
    if (fn)
        wallet.patchFn = fn
    else
        wallet.patchFn = null
    socket.emit('investWallet', {
            'walletId': walletId,
            'money': money
        }
    )
}

socket.on('investWallet', function (data) {
    socket.patchJson = data
    if (wallet.patchFn)
        wallet.patchFn(data)
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
