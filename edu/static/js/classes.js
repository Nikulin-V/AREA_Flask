/*
 * Nikulin Vasily © 2021
 */

renderPage()

function renderPage() {
    classes.get(renderClassesTable)
}

function renderClassesTable() {
    table = document.getElementById('classes-table-span')
    if (table)
        while (table.children.length > 0)
            table.removeChild(table.children[0])

    classesTable = document.createElement('table')
    classesTable.id = "classes-table"
    classesTable.className = "dairy-table table-hover table-info"

    if (classes.getJson['classes'].length > 0) {
        classesTableCaption = document.createElement('caption')
        classesTableCaption.style.captionSide = "top"
        classesTableCaption.textContent = "Классы"

        classesTable.appendChild(classesTableCaption)

        classesTableThead = document.createElement('thead')
        classesTableThead.style.backgroundColor = "#86CFDA"
        classesTableTheadClassNumber = document.createElement('td')
        classesTableTheadClassNumber.textContent = "Номер"
        classesTableTheadClassNumber.style.textAlign = "center"
        classesTableTheadClassNumber.style.padding = "5px"
        classesTableTheadClassLetter = document.createElement('td')
        classesTableTheadClassLetter.textContent = "Литера"
        classesTableTheadClassLetter.style.textAlign = "center"
        classesTableTheadClassLetter.style.padding = "5px"
        classesTableThead.appendChild(classesTableTheadClassNumber)
        classesTableThead.appendChild(classesTableTheadClassLetter)
        classesTableTbody = document.createElement('tbody')

        classesList = classes.getJson['classes']

        for (let classId = 0; classId < classesList.length; classId++) {
            const row = document.createElement('tr')

            row.onclick = function () {
                editClass(this.number, this.letter)
            }
            row.addEventListener("mouseout", function () {
                clicked = false
                renderPage()

                this.onmouseup = function () {
                    editClass(this.number, this.letter)
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
                    editClass(this.number, this.letter)
                }
                this.appendChild(td)
            })

            td1 = document.createElement('td')
            td1.textContent = classesList[classId]['number']
            row.number = classesList[classId]['number']
            td1.style.textAlign = "center"
            row.appendChild(td1)

            td2 = document.createElement('td')
            td2.textContent = classesList[classId]['letter']
            row.letter = classesList[classId]['letter']
            td2.style.textAlign = "center"
            row.appendChild(td2)

            classesTableTbody.appendChild(row)
        }

        classesTable.appendChild(classesTableThead)
        classesTable.appendChild(classesTableTbody)
    } else {

        classesTableThead = document.createElement('thead')
        classesTableThead.style.backgroundColor = "#86CFDA"
        classesTableTheadNotclasses = document.createElement('td')
        classesTableTheadNotclasses.textContent = "Классов нет"
        classesTableTheadNotclasses.style.textAlign = "center"
        classesTableTheadNotclasses.style.padding = "5px"
        classesTableThead.appendChild(classesTableTheadNotclasses)
        classesTable.appendChild(classesTableThead)
    }
    document.getElementById('classes-table-span').appendChild(classesTable)
}

function createClass() {
    message =
        `<div>
            <div class="form-floating">
                <input type="number" min="1" max="11" id="number-input" class="form-control" placeholder="Номер класса" autocomplete="off">
                <label for="number-input">Номер класса</label>
            </div>
            <br>
            <div class="form-floating">
                <input maxlength="1" id="letter-input" class="form-control" placeholder="Литера класса" autocomplete="off">
                <label for="letter-input">Литера класса</label>
            </div>
        </div>`
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
}

function editClass(number = null,
                   letter = null) {
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
        const new_number = document.getElementById('number-input').value
        const new_letter = document.getElementById('letter-input').value

        classes.put(old_number, old_letter, new_number, new_letter, renderPage)
        closeModal()
    }
    showModal(message, 'Новый класс', [buttonSave, buttonDelete])
}