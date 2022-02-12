/*
 * Nikulin Vasily © 2021
 */

renderPage()

function renderPage() {
    info.teachersList()
    classes.get(renderClassesTable)
}

function renderClassesTable() {
    table = document.getElementById('classes-table')
    if (table)
        while (table.children.length > 0)
            table.removeChild(table.children[0])

    if (classes.getJson['classes'].length > 0) {
        classesList = classes.getJson['classes']

        for (let classId = 0; classId < classesList.length; classId++) {
            const number = classesList[classId]['number']
            const letter = classesList[classId]['letter']
            const teacher = classesList[classId]['teacher']
            cardId = `edit-${number + letter}`

            card = `
                <div class="col col-lg-3">
                    <div class="card text-center border-info">
                      <div class="card-body">
                        <h2 class="card-title">${number + letter}</h2>
                        <p class="card-subtitle text-secondary">
                            ${typeof teacher == "string" ? teacher.split(' ')[0] + ' ' + teacher.split(' ')[1][0] + '. ' + teacher.split(' ')[2][0] + '. ' : 'Не назначен'}
                        </p>
                        <br>
                        <div class="btn-group" role="group">
                          <a type="button" href="${window.location.origin + '/workload?classNumber=' + number + '&classLetter=' + letter}" class="btn btn-outline-info" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-delay="400" title="Нагрузка">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-activity" viewBox="0 0 16 16">
                                <path fill-rule="evenodd" d="M6 2a.5.5 0 0 1 .47.33L10 12.036l1.53-4.208A.5.5 0 0 1 12 7.5h3.5a.5.5 0 0 1 0 1h-3.15l-1.88 5.17a.5.5 0 0 1-.94 0L6 3.964 4.47 8.171A.5.5 0 0 1 4 8.5H.5a.5.5 0 0 1 0-1h3.15l1.88-5.17A.5.5 0 0 1 6 2Z"/>
                            </svg>
                          </a>
                          <a type="button" id="${cardId}" class="btn btn-outline-danger" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-delay="400"  title="Изменить">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
                              <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
                            </svg>
                          </a>
                        </div>
                      </div>
                    </div>
                </div>`

            card.number = number
            card.letter = letter
            card.teacher = teacher

            table.insertAdjacentHTML('beforeend', card)

            const editButton = document.getElementById(cardId)
            editButton.letter = letter
            editButton.number = number
            editButton.teacher = teacher
            editButton.onclick = function () {
                editClass(this.number, this.letter, this.teacher)
            }

        }

    }

    let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

}

function createClass() {
    message =
        `<div>
            <div class="form-floating" >
                <input type="number" min="1" max="11" id="number-input" class="form-control" 
                       placeholder="Номер класса" autocomplete="off">
                <label for="number-input">Номер класса</label>
            </div>
            <br>
            <div class="form-floating">
                <input maxlength="1" id="letter-input" class="form-control"
                       placeholder="Литера класса" autocomplete="off">
                <label for="letter-input">Литера класса</label>
            </div>
            <br>
            <div class="form-floating">
                <select id="teacher-select" class="form-control" placeholder="Классный руководитель">
                    <option value="${null}">Не назначен</option>
                </select>
                <label for="teacher-select">Классный руководитель</label>
            </div>
        </div>
        `
    button = document.createElement('button')
    button.textContent = "Добавить"
    button.className = "btn btn-info"


    button.onclick = function () {
        const number = document.getElementById('number-input').value
        const letter = document.getElementById('letter-input').value

        classes.post(number, letter, renderPage)
        closeModal()
    }
    showModal(message, 'Новый класс', [button])

    let teacherSelect = $('#teacher-select')
    fillSelectField(teacherSelect, info.teachersListJson['teachers'])
    document.getElementById('teacher-select').selectedIndex = 0
}

function editClass(number = null,
                   letter = null,
                   teacher = null) {
    message =
        `<div>
            <div class="form-floating">
                <input type="number" min="1" max="11" id="number-input" class="form-control" value="${number}" placeholder="Номер класса" autocomplete="off">
                <label for="number-input">Номер класса</label>
            </div>
            <br>
            <div class="form-floating">
                <input maxlength="1" id="letter-input" class="form-control" value="${letter}" placeholder="Литера класса" autocomplete="off">
                <label for="letter-input">Литера класса</label>
            </div>
            <br>
            <div class="form-floating">
                <select id="teacher-select" class="form-control" placeholder="Классный руководитель">
                    <option value="${null}">Не назначен</option>
                </select>
                <label for="teacher-select">Классный руководитель</label>
            </div>
        </div>`

    buttonDelete = document.createElement('button')
    buttonDelete.textContent = "Удалить"
    buttonDelete.className = "btn btn-danger"

    buttonDelete.onclick = function () {
        const number = document.getElementById('number-input').value
        const letter = document.getElementById('letter-input').value

        classes.delete(number, letter, renderPage)
        closeModal()
    }

    buttonSave = document.createElement('button')
    buttonSave.textContent = "Сохранить"
    buttonSave.className = "btn btn-info"

    buttonSave.onclick = function () {
        const old_number = number
        const old_letter = letter
        const old_teacher = teacher
        const new_number = document.getElementById('number-input').value
        const new_letter = document.getElementById('letter-input').value
        const new_teacher = document.getElementById('teacher-select').value

        classes.put(old_number, old_letter, old_teacher, new_number, new_letter, new_teacher, renderPage)
        closeModal()
    }
    showModal(message, 'Новый класс', [buttonSave, buttonDelete])

    let teacherSelect = $('#teacher-select')
    fillSelectField(teacherSelect, info.teachersListJson['teachers'])
    teacherSelect.val(teacher)

    if (teacher == null)
        document.getElementById('teacher-select').selectedIndex = 0
}

function fillSelectField(field, list) {
    for (let i = 0; i < list.length; i++) {
        let option = new Option(list[i], list[i])
        field.append(option)
    }
}