/*
 * Nikulin Vasily © 2021
 */

renderPage()

function renderPage() {
    info.subjects()
    info.teachersList()
    workload.get(...getClassNumberAndLetter(), renderWorkloadTable)
}

function getClassNumberAndLetter() {
    let classTitle = document.querySelector("body > main > table > tbody > tr > td:nth-child(1) > " + (!isMobile() ? 'h1' : 'h3')).innerText.split(' ')[2]
    let classNumber = classTitle.slice(0, classTitle.length - 1)
    let classLetter = classTitle[classTitle.length - 1]
    return [classNumber, classLetter]
}

function renderWorkloadTable() {
    let table = document.getElementById('workload-table-span')
    let totalDiv = document.getElementById('total-div')
    if (table)
        while (table.children.length > 0)
            table.removeChild(table.children[0])

    if (totalDiv)
        while (totalDiv.children.length > 0)
            totalDiv.removeChild(totalDiv.children[0])

    let workloadTable = document.createElement('table')
    workloadTable.id = "workload-table"
    workloadTable.className = "dairy-table table-hover table-info stocks-table"

    if (workload.getJson['workload'].length > 0) {
        let workloadTableCaption = document.createElement('caption')
        workloadTableCaption.style.captionSide = "top"
        workloadTableCaption.textContent = "Почасовая нагрузка"

        workloadTable.appendChild(workloadTableCaption)

        let workloadTableThead = document.createElement('thead')
        workloadTableThead.style.backgroundColor = "#86CFDA"
        let workloadTableTheadSubject = document.createElement('td')
        workloadTableTheadSubject.textContent = "Предмет"
        workloadTableTheadSubject.style.textAlign = "center"
        workloadTableTheadSubject.style.padding = "5px"
        let workloadTableTheadTeacher = document.createElement('td')
        workloadTableTheadTeacher.textContent = "Учитель"
        workloadTableTheadTeacher.style.textAlign = "center"
        workloadTableTheadTeacher.style.padding = "5px"
        let workloadTableTheadHours = document.createElement('td')
        workloadTableTheadHours.textContent = "Часы"
        workloadTableTheadHours.style.textAlign = "center"
        workloadTableTheadHours.style.padding = "5px"
        let workloadTableTheadGroupNumber = document.createElement('td')
        workloadTableTheadGroupNumber.textContent = "Группа"
        workloadTableTheadGroupNumber.style.textAlign = "center"
        workloadTableTheadGroupNumber.style.padding = "5px"
        workloadTableThead.appendChild(workloadTableTheadSubject)
        workloadTableThead.appendChild(workloadTableTheadTeacher)
        workloadTableThead.appendChild(workloadTableTheadHours)
        workloadTableThead.appendChild(workloadTableTheadGroupNumber)
        let workloadTableTbody = document.createElement('tbody')

        let workloadList = workload.getJson['workload']

        for (let workloadId = 0; workloadId < workloadList.length; workloadId++) {
            const row = document.createElement('tr')

            row.onclick = function () {
                editWorkload(...getClassNumberAndLetter(), this.teacher, this.title, this.hours, this.groupNumber)
            }
            row.addEventListener("mouseout", function () {
                clicked = false
                renderPage()

                this.onmouseup = function () {
                    editWorkload(...getClassNumberAndLetter(), this.teacher, this.title, this.hours, this.groupNumber)
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
                    editWorkload(...getClassNumberAndLetter(), this.teacher, this.title, this.hours, this.groupNumber)
                }
                this.appendChild(td)
            })

            let td1 = document.createElement('td')
            td1.textContent = workloadList[workloadId]['title']
            row.title = workloadList[workloadId]['title']
            td1.style.textAlign = "center"
            row.appendChild(td1)

            let td2 = document.createElement('td')
            td2.textContent = workloadList[workloadId]['teacher'] ? workloadList[workloadId]['teacher'] : '—'
            row.teacher = workloadList[workloadId]['teacher']
            td2.style.textAlign = "center"
            row.appendChild(td2)

            let td3 = document.createElement('td')
            td3.textContent = workloadList[workloadId]['hours']
            row.hours = workloadList[workloadId]['hours']
            td3.style.textAlign = "center"
            row.appendChild(td3)

            let td4 = document.createElement('td')
            td4.textContent = workloadList[workloadId]['groupNumber'] === 0 ? '—' : workloadList[workloadId]['groupNumber']
            row.groupNumber = td4.textContent !== '—' ? td4.textContent : 0
            td4.style.textAlign = "center"
            row.appendChild(td4)

            workloadTableTbody.appendChild(row)
        }

        workloadTable.appendChild(workloadTableThead)
        workloadTable.appendChild(workloadTableTbody)

        totalDiv.innerHTML = `
        <h5>Часы: ${workload.getJson['hours']}</h5>
        <h5>Человекочасы: ${workload.getJson['manHours']}</h5>
        `
    } else {

        let workloadTableThead = document.createElement('thead')
        workloadTableThead.style.backgroundColor = "#86CFDA"
        let workloadTableTheadNotWorkload = document.createElement('td')
        workloadTableTheadNotWorkload.textContent = "Нет записей"
        workloadTableTheadNotWorkload.style.textAlign = "center"
        workloadTableTheadNotWorkload.style.padding = "5px"
        workloadTableThead.appendChild(workloadTableTheadNotWorkload)
        workloadTable.appendChild(workloadTableThead)
    }

    spinner = document.getElementById('spinner')
    if (spinner)
        table.removeChild(table.children[0])

    document.getElementById('workload-table-span').appendChild(workloadTable)
}

function createWorkload() {
    let message =
        `<div>
            <div class="form-floating">
                <select id="title-select" class="form-control" placeholder="Предмет"></select>
                <label for="title-select">Предмет</label>
            </div>
            <br>
            <div class="form-floating">
                <select id="teacher-select" class="form-control" placeholder="Учитель">
                    <option value="${null}">Не назначен</option>
                </select>
                <label for="teacher-select">Учитель</label>
            </div>
            <br>
            <div class="form-floating">
                <input id="hours-input" type="number" min="1" class="form-control" placeholder="Часы" autocomplete="off">
                <label for="hours-input">Часы</label>
            </div>
            <br>
            <div class="form-floating">
                <input id="group-number-input" class="form-control" placeholder="Номер группы" autocomplete="off">
                <label for="group-number-input">Номер группы</label>
            </div>
        </div>`

    let button = document.createElement('button')
    button.textContent = "Добавить"
    button.className = "btn btn-info"

    button.onclick = function () {
        let subject = document.getElementById('title-select').value
        let teacher = document.getElementById('teacher-select').value
        let hours = document.getElementById('hours-input').value
        let groupNumber = document.getElementById('group-number-input').value
        groupNumber = groupNumber ? groupNumber : 0

        workload.post(...getClassNumberAndLetter(), teacher, subject, hours, groupNumber, renderPage)
        closeModal()
    }

    showModal(message, 'Новая запись', [button])
    fillSelectField($('#title-select'), info.subjectsJson['subjects'])
    fillSelectField($('#teacher-select'), info.teachersListJson['teachers'])
}

function editWorkload(classNumber = null,
                      classLetter = null,
                      oldTeacher = null,
                      oldTitle = null,
                      oldHours = 0,
                      oldGroupNumber = 0) {
    let message =
        `<div>
            <div class="form-floating">
                <select id="title-select" class="form-control" placeholder="Предмет"></select>
                <label for="title-select">Предмет</label>
            </div>
            <br>
            <div class="form-floating">
                <select id="teacher-select" class="form-control" placeholder="Учитель"">
                    <option value="${null}">Не назначен</option>
                </select>
                <label for="teacher-select">Учитель</label>
            </div>
            <br>
            <div class="form-floating">
                <input id="hours-input" type="number" min="0" class="form-control" placeholder="Часы" autocomplete="off" value="${oldHours}">
                <label for="hours-input">Часы</label>
            </div>
            <br>
            <div class="form-floating">
                <input id="group-number-input" class="form-control" placeholder="Номер группы" autocomplete="off" value="${oldGroupNumber !== 0 ? oldGroupNumber : ''}">
                <label for="group-number-input">Номер группы</label>
            </div>
        </div>`

    buttonDelete = document.createElement('button')
    buttonDelete.textContent = "Удалить"
    buttonDelete.className = "btn btn-danger"

    buttonDelete.onclick = function () {
        workload.delete(...getClassNumberAndLetter(), oldTeacher, oldTitle, oldHours, oldGroupNumber, renderPage)
        closeModal()
    }

    buttonSave = document.createElement('button')
    buttonSave.textContent = "Сохранить"
    buttonSave.className = "btn btn-info"

    buttonSave.onclick = function () {
        let title = document.getElementById('title-select').value
        let teacher = document.getElementById('teacher-select').value
        let hours = document.getElementById('hours-input').value
        let groupNumber = document.getElementById('group-number-input').value
        groupNumber = groupNumber ? groupNumber : 0

        workload.put(...getClassNumberAndLetter(), oldTeacher, oldTitle, oldHours, oldGroupNumber,
            teacher, title, hours, groupNumber, renderPage)
        closeModal()
    }

    showModal(message, 'Изменение записи', [buttonSave, buttonDelete])

    let subjectSelect = $('#title-select')
    let teacherSelect = $('#teacher-select')
    fillSelectField(subjectSelect, info.subjectsJson['subjects'])
    fillSelectField(teacherSelect, info.teachersListJson['teachers'])
    subjectSelect.val(oldTitle)
    teacherSelect.val(oldTeacher)

    if (oldTeacher == null)
        document.getElementById('teacher-select').selectedIndex = 0
}

function fillSelectField(field, list) {
    for (let i = 0; i < list.length; i++) {
        let option = new Option(list[i], list[i])
        field.append(option)
    }
}

function isMobile() {
    let check = false;
    (function (a) {
        if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4))) check = true;
    })(navigator.userAgent || navigator.vendor || window.opera);
    return check;
}