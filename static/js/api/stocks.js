/*
 * Nikulin Vasily © 2021
 */

/*
 * Nikulin Vasily © 2021 
 */

let stocks = Object()

stocks.get = function (fn=null) {
    if (fn)
        stocks.getFn = fn
    else
        stocks.getFn = null
    socket.emit('getStocks')
}

socket.on('getStocks', function (data) {
    stocks.getJson = data
    if (stocks.getFn)
        stocks.getFn()
})