// noinspection JSUnresolvedVariable,JSUnusedGlobalSymbols

gapi.load('client', {
    callback: function() {
        gapi.client.init()
    },
    onerror: function() {
        // Handle loading error.
        alert('gapi.client failed to load!');
    },
    timeout: 5000, // 5 seconds.
    ontimeout: function() {
        // Handle timeout.
        alert('gapi.client could not load in a timely manner!');
    }
});
