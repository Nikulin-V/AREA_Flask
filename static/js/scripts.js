/*
 * Nikulin Vasily © 2021
 */

// noinspection JSUnresolvedFunction

let dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
dropdownElementList.map(function (dropdownToggleEl) {
    return new bootstrap.Dropdown(dropdownToggleEl)
});

// let pageUrl = document.location.pathname
// if (pageUrl === "/" || pageUrl === "/index" || pageUrl === "/privacy-policy") {
//     document.body.style.background = "url('/static/images/index-background.jpg') fixed"
// }



let myModal = document.getElementById('myModal');
let myInput = document.getElementById('myInput');

if (myModal && myInput) {
    myModal.addEventListener('shown.bs.modal', function () {
        myInput.focus()
})
}

let modal_close_btn = document.getElementById('modal-close-btn')
if (modal_close_btn) {
    modal_close_btn.onclick = function () {
        $("#myModal").modal('hide');
    }
}

let modal_ok_btn = document.getElementById('modal-ok-btn')
if (modal_ok_btn) {
    modal_ok_btn.onclick = function () {
        $("#myModal").modal('hide');
    }
}

// Homework spinner
let homework_link = document.getElementById('epos-diary')
if (homework_link) {
    homework_link.onclick = function () {
        let homework_spinner = document.getElementById('epos-spinner')
        homework_spinner.style.visibility = "visible"
    }
}

/**
 * @param {String | HTMLElement} message
 * @param {string} title
 * @param {HTMLButtonElement[]|HTMLButtonElement} buttons
 * @param {boolean} isBuyMode
 */
function showModal(message,
                   title='Сообщение от сайта',
                   buttons=null,
                   isBuyMode=false)
{
    if (buttons === null){
        button = document.createElement('button')
        button.type = 'button'
        button.className = "btn btn-info"
        button.onclick = closeModal
        button.textContent = 'OK'
        buttons = [button]
    }

    modalHTML = `<!-- Всплывающее сообщение -->
    <div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="modal-title"></h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                </div>
                <div class="modal-footer" id="modal-btn">
                </div>
            </div>
        </div>
    </div>`
    document.body.insertAdjacentHTML('beforeend', modalHTML)

    modalFooter = document.getElementById('modal-btn')
    while (modalFooter.children.length > 0)
        modalFooter.children[0].remove()
    for (buttonId = 0; buttonId < buttons.length; buttonId++) {
        modalFooter.appendChild(buttons[buttonId])
    }


    modalTitle = document.getElementById('modal-title')
    modalTitle.textContent = title

    modal = document.getElementById('myModal')
    modalBody = modal.getElementsByClassName('modal-body')[0]
    while (modalBody.children.length > 0)
        modalBody.children[0].remove()

    if ((typeof message) === 'object')
        modalBody.appendChild(message)
    else
        modalBody.innerHTML = message

    $("#myModal").modal('show');

    if (isBuyMode) {
        modal = document.getElementsByClassName('modal-backdrop')[0]
        modal.onclick = function () {
            clearTimeout(timeoutId)
            offers.put(null, null, 'decline', offers.putJson, closeModalAndRenderPage)
        }
        buttonClose = document.getElementsByClassName('btn-close')[0]
        buttonClose.onclick = function () {
            clearTimeout(timeoutId)
            offers.put(null, null, 'decline', offers.putJson, closeModalAndRenderPage)
        }
    }
}
function closeModal() {
    shadow = document.getElementsByClassName('modal-backdrop fade show')
    if (shadow.length > 0)
        $("#myModal").modal('toggle');
}

function createParagraph(message) {
    p = document.createElement('p')
    p.textContent = message
    return p
}

function fillCompanies () {
    stocksJson = stocks.getJson['stocks']
    for (companyId = 0; companyId < stocksJson.length; companyId++) {
        companyTitle = stocksJson[companyId]['company']
        $("#companies-select").append(new Option(companyTitle, companyTitle))
    }
}

function closeModalAndRenderPage() {
    closeModal()
    renderPage()
}

function showNotifications(logoSource, author = null, company = null, date, time, message = null, redirectLink = '#') {
    id = redirectLink.split('#')[1]
    let newsEvents = ['post_add', 'domain_disabled', 'addchart', 'business']
    if (!(logoSource === 'rule' && window.location.pathname === '/companies-management'))
        if (logoSource === 'rule')
            svotes.get(function (data) {
                svotesList = data['votes']
                if (svotesList.length > 0)
                    if (svotesList[svotesList.length - 1]['id'] === id)
                        showNotificationAction(logoSource, author, company, date, time, message, redirectLink)
            })
        else if (newsEvents.indexOf(logoSource) !== -1 && window.location.pathname === '/news') {
            showNewPostsBtn()
            if (logoSource !== 'post_add')
                showNotificationAction(logoSource, author, company, date, time, message, redirectLink)
        } else showNotificationAction(logoSource, author, company, date, time, message, redirectLink)
}

function showNotificationAction(logoSource, author = null, company = null, date, time, message = null, redirectLink = '#') {
    notificationsDiv = document.getElementById('notifications')
    if (company && author) {
        td1 = `<td style="text-align: center">
                        <a class="normal-link" href="${redirectLink}">
                            <b>${company}</b>
                        </a>
                   </td>`
        td2 = `<td style="text-align: center">
                        <a class="normal-link" href="${redirectLink}">
                            ${author}
                        </a>
                   </td>`
    } else {
        td2 = ''
        if (company)
            td1 = `<td rowspan="2" style="text-align: center">
                        <a class="normal-link" href="${redirectLink}">
                            <b>${company}</b>
                        </a>
                   </td>`
        if (author)
            td1 = `<td rowspan="2" style="text-align: center">
                        <a class="normal-link" href="${redirectLink}">
                            <b>${author}</b>
                        </a>
                   </td>`
    }
    if (message)
        messageDiv =
            `
            <div class="toast-body">
                ${message}  
            </div>
            `
    else messageDiv = ''
    notificationsDiv.insertAdjacentHTML('beforeend',
        `
            <div role="alert" aria-live="polite" aria-atomic="true" class="toast" data-bs-delay="7000">
              <div class="toast-header">
                <table class="layout-table" style="width: 100%">
                    <tr>
                        <td rowspan="2"><span class="material-icons-round notification-icon">${logoSource}</span></td>
                        ${td1}
                        <td rowspan="2" style="text-align: right; white-space: nowrap"><small>${date} | ${time}</small></td>
                    </tr>
                    <tr>
                        ${td2}
                    </tr>
                </table>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Закрыть"></button>
              </div>
              ${messageDiv}
            </div>
        `)
    let toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl)
    });
    notification = toastList[toastList.length - 1]
    notification.show()
}

function showNewPostsBtn() {
    document.getElementById('news-update-btn').style.display = "block"
}

function showConnected(connected = true) {
    const monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    let now = new Date()
    let date = monthNames[now.getMonth()] + ' ' + now.getDate().toString()
    let time = now.toLocaleString().split(', ')[1].slice(-8, -3)
    let logoSource = connected ? 'wifi' : 'wifi_off'
    let message = connected ? 'Соединение восстановлено' : 'Соединение разорвано'
    showNotifications(logoSource, message, 'AREA', date, time)
}