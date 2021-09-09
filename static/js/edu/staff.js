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
        staffTableTheadPatronymic = document.createElement('td')
        staffTableTheadPatronymic.textContent = "Отчество"
        staffTableTheadPatronymic.style.textAlign = "center"
        staffTableTheadPatronymic.style.padding = "5px"
        staffTableTheadisTeacher = document.createElement('td')
        staffTableTheadisTeacher.textContent = "Учитель"
        staffTableTheadisTeacher.style.textAlign = "center"
        staffTableTheadisTeacher.style.padding = "5px"
        staffTableTheadisHeadTeacher = document.createElement('td')
        staffTableTheadisHeadTeacher.textContent = "Завуч"
        staffTableTheadisHeadTeacher.style.textAlign = "center"
        staffTableTheadisHeadTeacher.style.padding = "5px"
        staffTableThead.appendChild(staffTableTheadSurname)
        staffTableThead.appendChild(staffTableTheadName)
        staffTableThead.appendChild(staffTableTheadPatronymic)
        staffTableThead.appendChild(staffTableTheadisTeacher)
        staffTableThead.appendChild(staffTableTheadisHeadTeacher)
        staffTableTbody = document.createElement('tbody')

        staff = teachers.getJson['users']

        for (let userId = 0; userId < staff.length; userId++) {
            const row = document.createElement('tr')

            row.onclick = function () {
                editTeacher(this.company, this.stocks)
            }
            row.addEventListener("mouseout", function () {
                clicked = false
                renderPage()

                this.onmouseup = function () {
                    editTeacher(this.surname, this.name, this.patronymic, this.isTeacher, this.isHeadTeacher)
                }
            })
            row.addEventListener("mousedown", function () {
                clicked = true
                while (this.children.length > 0)
                    this.removeChild(this.children[0])
                const td = document.createElement('td')
                td.style.textAlign = "center"
                td.textContent = "Редактировать"
                td.colSpan = 5
                this.onmouseup = function () {
                    clicked = false
                    editTeacher(this.surname, this.name, this.patronymic, this.isTeacher, this.isHeadTeacher)
                }
                this.appendChild(td)
            })

            td1 = document.createElement('td')
            td1.textContent = staff[userId]['surname']
            row.surname = staff[userId]['surname']
            td1.style.textAlign = "center"
            row.appendChild(td1)

            td2 = document.createElement('td')
            td2.textContent = staff[userId]['name']
            row.name = staff[userId]['name']
            td2.style.textAlign = "center"
            row.appendChild(td2)

            td3 = document.createElement('td')
            td3.textContent = staff[userId]['patronymic']
            row.patronymic = staff[userId]['patronymic']
            td3.style.textAlign = "center"
            row.appendChild(td3)

            td4 = document.createElement('td')
            td4.textContent = staff[userId]['roles'].indexOf("teacher") !== -1 ? '✔' : '❌'
            row.isTeacher = staff[userId]['roles'].indexOf("teacher") !== -1
            td4.style.textAlign = "center"
            row.appendChild(td4)

            td5 = document.createElement('td')
            td5.textContent = staff[userId]['roles'].indexOf("head_teacher") !== -1 ? '✔' : '❌'
            row.isHeadTeacher = staff[userId]['roles'].indexOf("head_teacher") !== -1
            td5.style.textAlign = "center"
            row.appendChild(td5)

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
                <input id="name-input" class="form-control" placeholder="Имя" autocomplete="off">
                <label for="name-input">Имя</label>
            </div>
            <br>
            <div class="form-floating">
                <input id="patronymic-input" class="form-control" placeholder="Отчество" autocomplete="off">
                <label for="patronymic-input">Отчество</label>
            </div>
            <br>
            <h5>Роли</h5>
            <div class="form-check">
                <input class="form-check-input" type="checkbox" id="teacher-input" checked>
                <label class="form-check-label" for="teacher-input">
                    Учитель
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="checkbox" id="head-teacher-input">
                <label class="form-check-label" for="head-teacher-input">
                    Завуч
                </label>
            </div>
        </div>`
    button = document.createElement('button')
    button.textContent = "Добавить"
    button.className = "btn btn-info"


    button.onclick = function () {
        const surname = document.getElementById('surname-input').value
        const name = document.getElementById('name-input').value
        const patronymic = document.getElementById('patronymic-input').value
        const isTeacher = document.getElementById('teacher-input').checked
        const isHeadTeacher = document.getElementById('head-teacher-input').checked

        if (surname && name) {
            let roles = ['user']
            if (isTeacher)
                roles.push('teacher')
            if (isHeadTeacher)
                roles.push('head_teacher')

            teachers.post(surname, name, patronymic, roles, renderPage)
            closeModal()
        }
    }
    showModal(message, 'Новый сотрудник', [button])
}

function editTeacher(surname = null,
                     name = null,
                     patronymic = null,
                     isTeacher = true,
                     isHeadTeacher = false) {
    message =
        `<div>
            <div class="form-floating">
                <input id="surname-input" class="form-control" placeholder="Фамилия" value="${surname}" autocomplete="off">
                <label for="surname-input">Фамилия</label>
            </div>
            <br>
            <div class="form-floating">
                <input id="name-input" class="form-control" placeholder="Имя" value="${name}" autocomplete="off">
                <label for="name-input">Имя</label>
            </div>
            <br>
            <div class="form-floating">
                <input id="patronymic-input" class="form-control" placeholder="Отчество" value="${patronymic}" autocomplete="off">
                <label for="patronymic-input">Отчество</label>
            </div>
            <br>
            <h5>Роли</h5>
            <div class="form-check">
                <input class="form-check-input" type="checkbox" id="teacher-input" ${isTeacher ? 'checked' : ''}>
                <label class="form-check-label" for="teacher-input">
                    Учитель
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="checkbox" id="head-teacher-input" ${isHeadTeacher ? 'checked' : ''}>
                <label class="form-check-label" for="head-teacher-input">
                    Завуч
                </label>
            </div>
        </div>`

    buttonDelete = document.createElement('button')
    buttonDelete.textContent = "Удалить"
    buttonDelete.className = "btn btn-danger"

    buttonDelete.onclick = function () {
        const surname = document.getElementById('surname-input').value
        const name = document.getElementById('name-input').value
        const patronymic = document.getElementById('patronymic-input').value
        const isTeacher = document.getElementById('teacher-input').checked
        const isHeadTeacher = document.getElementById('head-teacher-input').checked

        if (surname && name) {
            let roles = ['user']
            if (isTeacher)
                roles.push('teacher')
            if (isHeadTeacher)
                roles.push('head_teacher')

            teachers.delete(surname, name, patronymic, roles, renderPage)
            closeModal()
        }
    }

    buttonSave = document.createElement('button')
    buttonSave.textContent = "Сохранить"
    buttonSave.className = "btn btn-info"

    buttonSave.onclick = function () {
        const surname = document.getElementById('surname-input').value
        const name = document.getElementById('name-input').value
        const patronymic = document.getElementById('patronymic-input').value
        const isTeacher = document.getElementById('teacher-input').checked
        const isHeadTeacher = document.getElementById('head-teacher-input').checked

        if (surname && name) {
            let roles = ['user']
            if (isTeacher)
                roles.push('teacher')
            if (isHeadTeacher)
                roles.push('head_teacher')

            teachers.put(surname, name, patronymic, roles, renderPage)
            closeModal()
        }
    }
    showModal(message, 'Новый сотрудник', [buttonSave, buttonDelete])
}