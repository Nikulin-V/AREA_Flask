/*
 * Nikulin Vasily © 2021
 */

/*
 * Nikulin Vasily © 2021
 */

companies.get(fillSectors)

function createCompany() {
    sector = document.getElementById('sector').value
    title = document.getElementById('title').value
    description = document.getElementById('description').value
    logoUrl = document.getElementById('logo-url').value

    companies.post(sector, title, description, logoUrl, showMessage)
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
    }
    if (postJson['message'] === 'Success'){
        button = document.createElement('button')
        button.type = 'button'
        button.className = "btn btn-info"
        button.onclick = function () {
            location.href = '/marketplace'
        }
        button.textContent = 'OK'
        showModal(createParagraph('Компания успешно открыта.'),
            'Сообщение от сайта',  button)
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