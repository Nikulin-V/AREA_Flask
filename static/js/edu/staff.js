/*
 * Nikulin Vasily © 2021
 */

// TODO: add creating teacher


renderPage()

function renderPage() {
    teachers.get(renderStaffTable)
}

function renderStaffTable() {
    table = document.getElementById('staff-table-span')
    if (table)
        while (table.children.length > 0)
            table.removeChild(table.children[0])

    staffTable = document.createElement('table')
    staffTable.id = "staff-table"
    staffTable.className = "dairy-table table-hover table-info stocks-table"

    if (teachers.getJson['users'].length > 0) {
        staffTableCaption = document.createElement('caption')
        staffTableCaption.style.captionSide = "top"
        staffTableCaption.textContent = "Персонал"

        staffTable.appendChild(staffTableCaption)

        staffTableThead = document.createElement('thead')
        staffTableThead.style.backgroundColor = "#86CFDA"
        staffTableTheadSurname = document.createElement('td')
        staffTableTheadSurname.textContent = "Фамилия"
        staffTableTheadSurname.style.textAlign = "center"
        staffTableTheadSurname.style.padding = "5px"
        staffTableTheadName = document.createElement('td')
        staffTableTheadName.textContent = "Имя"
        staffTableTheadName.style.textAlign = "center"
        staffTableTheadName.style.padding = "5px"
        staffTableThead.appendChild(staffTableTheadSurname)
        staffTableThead.appendChild(staffTableTheadName)
        staffTableTbody = document.createElement('tbody')

        staff = teachers.getJson['users']

        for (let userId = 0; userId < staff.length; userId++) {
            const row = document.createElement('tr')

            td1 = document.createElement('td')
            td1.textContent = staff[userId]['surname']
            row.surname = staff[userId]['surname']
            td1.style.textAlign = "center"
            td2 = document.createElement('td')
            td2.textContent = staff[userId]['name']
            row.stocks = staff[userId]['name']
            td2.style.textAlign = "center"

            row.appendChild(td1)
            row.appendChild(td2)
            staffTableTbody.appendChild(row)
        }

        staffTable.appendChild(staffTableThead)
        staffTable.appendChild(staffTableTbody)
    } else {

        staffTableThead = document.createElement('thead')
        staffTableThead.style.backgroundColor = "#86CFDA"
        staffTableTheadNotStaff = document.createElement('td')
        staffTableTheadNotStaff.textContent = "Персонала нет"
        staffTableTheadNotStaff.style.textAlign = "center"
        staffTableTheadNotStaff.style.padding = "5px"
        staffTableThead.appendChild(staffTableTheadNotStaff)
        staffTable.appendChild(staffTableThead)
    }
    document.getElementById('staff-table-span').appendChild(staffTable)
}

function createTeacher() {
    message =
        `<div>
            <div class="form-floating">
                <input id="surname-input" class="form-control" placeholder="Фамилия" autocomplete="off">
                <label for="surname-input">Фамилия</label>
            </div>
            <br>
            <div class="form-floating">
                <input id="name-input" class="form-control" placeholder="Имя">
                <label for="name-input">Имя</label>
            </div>
            <br>
            <div class="form-floating">
                <input id="patronymic-input" class="form-control" placeholder="Отчество" autocomplete="off">
                <label for="patronymic-input">Отчество</label>
            </div>
            <br>
            
        </div>`
    button = document.createElement('button')
    button.textContent = "Добавить"
    button.className = "btn btn-info"


    button.onclick = function () {
        const title = document.getElementById('surname-input').value
        if (title) {

            if (document.getElementById('patronymic-input').files.length === 0) {
                const surname = document.getElementById('surname-input').value
                const name = document.getElementById('name-input').value
                const patronymic = document.getElementById('patronymic-input').value

                teachers.post(surname, name, patronymic, renderPage)
                closeModal()
            } else {

                button.style.display = "none"

            }
        } else document.getElementById('surname-input').classList.add('is-invalid')
    }
    showModal(message, 'Новый сотрудник', [button])
}