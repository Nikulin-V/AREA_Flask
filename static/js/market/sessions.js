/*
 * Nikulin Vasily © 2021
 */

setTimeout(fillSessions, 100)
sessionSelect = document.getElementById('session-select')
sessionSelect.onchange = function () {
    sessionId = sessionSelect.options[sessionSelect.selectedIndex].value
    users.put(sessionId)
    fillSessions()
}

function createSession() {
    newSessionTitle = document.getElementById('new-session-input').value
    if (newSessionTitle !== '')
        sessions.post(newSessionTitle, function (data) {
            if (data['message'] === 'Success')
                fillSessions(function () {
                    sessionSelect.selectedIndex = sessionSelect.options.length - 1
                    sessionId = sessionSelect.options[sessionSelect.selectedIndex].value
                    users.put(sessionId)
                    document.getElementById('new-session-input').value = ''
                })
            else if (data['errors'][0] === 'This title has taken.')
                showModal(createParagraph(_('Это название занято.')))
        })
    else showModal(createParagraph(_('Укажите имя новой фондовой биржи.')))
}

function deleteSession() {
    isAcceptedElement = document.getElementById('delete-session-checkbox')
    isAccepted = isAcceptedElement.checked
    if (isAccepted)
        sessions.delete()
    isAcceptedElement.checked = false
}

function fillSessions(fn = null) {
    sessions.get(null, function (data) {
        sessionSelect = document.getElementById('session-select')
        while (sessionSelect.options.length > 0)
            sessionSelect.removeChild(sessionSelect.options[0])
        sessionsList = data['sessions']
        for (sessionId = 0; sessionId < sessionsList.length; sessionId++) {
            option = document.createElement('option')
            option.value = sessionsList[sessionId]['id']
            option.textContent = sessionsList[sessionId]['title']
            if (option.value === data['currentSession']['id'])
                option.selected = true
            sessionSelect.appendChild(option)
        }

        deleteSessionDiv = document.getElementById('delete-session')
        deleteSessionDiv.style.display = data["isAdmin"] ? "block" : "none"

        adminLinksDiv = document.getElementById('admin-links')
        adminLinksDiv.style.display = data["isAdmin"] ? "block" : "none"

        if (fn)
            fn()
    })

}

function renderPage() {
    fillSessions()
}