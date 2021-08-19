/*
 * Nikulin Vasily © 2021
 */

// noinspection JSUnresolvedFunction
if (typeof sessions !== 'undefined')
    sessions.get(null, function (data) {
        adminLinksDiv = document.getElementById('admin-links')
        adminLinksDiv.style.display = data["isAdmin"] ? "block" : "none"
    })

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
 * @param {HTMLButtonElement[]|HTMLButtonElement|String[]|String} buttons
 * @param {boolean} isBuyMode
 */
function showModal(message,
                   title = 'Сообщение от сайта',
                   buttons = null,
                   isBuyMode = false) {
    if (buttons === null) {
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
        if ((typeof buttons[buttonId]) === 'object')
            modalFooter.appendChild(buttons[buttonId])
        else
            modalFooter.insertAdjacentHTML('beforeend', buttons[buttonId])
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

function fillCompanies() {
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

function isMobile() {
    let check = false;
    (function (a) {
        if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4))) check = true;
    })(navigator.userAgent || navigator.vendor || window.opera);
    return check;
}