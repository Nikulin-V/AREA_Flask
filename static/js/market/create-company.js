/*
 * Nikulin Vasily © 2021
 */

companies.get(fillSectors)

function createCompany(button) {
    let sector = document.getElementById('sector').value
    let title = document.getElementById('title').value
    let description = document.getElementById('description').value

    if (document.getElementById('logo').files.length === 0) {
        companies.post(sector, title, description, null, showMessage)
    } else {
        let progressBar = document.getElementById("progressBar")
        let progressBarBack = document.getElementById("progressBarBack")

        let image = document.getElementById('logo').files[0]

        button.disabled = true
        progressBarBack.style.removeProperty("display")

        companies.uploadImage(image, (progress) => {
            progressBar.style.width = progress + "%"
            progressBar.setAttribute("aria-valuemin", progress.toString())
        }, (data) => {
            if (data["error"]) {
                document.getElementById('logo').classList.add('is-invalid')
                if (data["code"] === 1001) {
                    document.getElementById('logo-feedback').textContent = "Неверный или небезопасный формат файла"
                }
                progressBarBack.style.display = "none"
                progressBar.style.width = "0%"
                progressBar.setAttribute("aria-valuemin", "0")
                button.disabled = false
            } else {
                companies.post(sector, title, description, data["path"], showMessage)
                progressBarBack.style.display = "none"
                progressBar.style.width = "0%"
                button.disabled = false
            }
        }, () => {
            document.getElementById('image-input').classList.add('is-invalid')
            document.getElementById('image-feedback').textContent = "Файл слишком большой, пожалуйста выберите файл менее 32МБ"
            progressBarBack.style.display = "none"
            progressBar.style.width = "0%"
            progressBar.setAttribute("aria-valuemin", "0")
            button.disabled = false
        })
    }
}

function showMessage() {
    postJson = companies.postJson
    if (postJson['message'] === 'Error') {
        if (postJson['errors'][0] === 'Specify the sector of company')
            showModal(createParagraph('Укажите отрасль компании'))
        if (postJson['errors'][0] === 'Specify the title of company')
            showModal(createParagraph('Укажите название компании'))
        if (postJson['errors'][0] === 'This title is already taken')
            showModal(createParagraph('Это название уже занято. Придумайте другое, ведь бренд должен быть уникальным)'))
        if (postJson['errors'][0] === 'You do not have enough money')
            showModal(createParagraph('На Вашем счёте недостаточно средств, чтобы заплатить взнос'))
        if (postJson['errors'][0] === 'File is unsafe or located on a foreign server')
            showModal(createParagraph('Файл небезопасный или находится на удаленном сервере'))
    }
    if (postJson['message'] === 'Success') {
        button = document.createElement('button')
        button.type = 'button'
        button.className = "btn btn-info"
        button.onclick = function () {
            location.href = '/marketplace'
        }
        button.textContent = 'OK'
        showModal(createParagraph('Компания успешно открыта.'),
            'Сообщение от сайта', button)
    }

}

function fillSectors() {
    sectors = Object.keys(companies.getJson['companies'])
    for (sectorId = 0; sectorId < sectors.length; sectorId++) {
        option = document.createElement('option')
        option.value = sectors[sectorId]
        option.textContent = sectors[sectorId]
        sector.appendChild(option)
    }
}

function valid(element) {
    if (element.classList.contains("is-invalid")) {
        element.classList.remove("is-invalid")
    }
}