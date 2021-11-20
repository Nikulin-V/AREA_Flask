/*
 * Nikulin Vasily © 2021
 */

renderPage()

function renderPage() {
    votes.get(createTable)
    companies.get()
}

function createTable() {
    let main = document.getElementsByTagName('main')[0]
    companiesTable = document.getElementsByClassName('companies-table')
    while (document.getElementsByClassName('companies-table').length > 0)
        main.removeChild(document.getElementsByClassName('companies-table')[0])

    votesJson = votes.getJson['votes']
    sectors = Object.keys(votesJson)

    companiesExist = false
    for (sectorId = 0; sectorId < sectors.length; sectorId++) {
        if (Object.keys(votesJson[sectors[sectorId]]).length > 0) {
            companiesExist = true
            const table = main.appendChild(document.createElement('table'));
            table.className = "companies-table dairy-table table-hover table-info"
            const caption = table.appendChild(document.createElement('caption'))
            caption.textContent = sectors[sectorId]
            caption.style.captionSide = "top"
            const thead = table.appendChild(document.createElement('thead'));
            thead.style.backgroundColor = "#86CFDA"
            const tr = thead.appendChild(document.createElement('tr'));

            tableData = []
            for (i = 0; i < Object.keys(votesJson[sectors[sectorId]]).length; i++) {
                v = votesJson[sectors[sectorId]][i]
                if (v["user_points"] === 0)
                    v["user_points"] = '-'
                tableData.push(
                    {
                        'Компания': v["company"],
                        'Общее доверие': v["points"],
                        'Ваше доверие': v["user_points"]
                    }
                )
            }

            let columnTexts = Object.keys(tableData[0]);
            columnTexts.forEach((columnText) => {
                const td = tr.appendChild(document.createElement('td'))
                td.textContent = columnText;
                td.style.textAlign = "center"
            });
            const tbody = table.appendChild(document.createElement('tbody'));
            tableData.forEach((voting) => {
                const tr = tbody.appendChild(document.createElement('tr'));
                const values = Object.values(voting);

                tr.className = "voting_row"
                tr.id = values[0].toString()

                tr.onclick = function () {

                    points = parseInt(document.getElementById('points').value)
                    votes.put(values[0], points, function (data) {
                        changeVotingValues(values[0], points, data)
                    })
                }

                values.forEach(value => {
                    const td = tr.appendChild(document.createElement('td'))
                    td.textContent = value.toString();
                    td.style.textAlign = 'center'
                });
            });
        }
    }

    if (!companiesExist) {
        main.insertAdjacentHTML('beforeend', `
        <table class="dairy-table table-hover table-info companies-table">
            <tr style="background-color: #86CFDA">
                <td style="text-align: center;padding: 5px">Нет компаний</td>
            </tr>
        </table>
        `)
        pointsInput = document.getElementById('points')
        pointsInput.disabled = true
    }

}

function changeVotingValues(companyTitle, points, data) {
    if (data['message'] === 'Success') {
        tr = document.getElementById(companyTitle)
        if (points === 0) {
            if (tr.children[2].textContent !== "-")
                tr.children[1].textContent = (parseInt(tr.children[1].textContent) -
                    parseInt(tr.children[2].textContent)).toString()
            tr.children[2].textContent = '-'
        } else {
            if (tr.children[2].textContent === "-")
                tr.children[1].textContent = (parseInt(tr.children[1].textContent) + points).toString()
            else
                tr.children[1].textContent = (parseInt(tr.children[1].textContent) -
                    parseInt(tr.children[2].textContent) + points).toString()
            tr.children[2].textContent = points.toString()
        }
    } else {

        if (data['errors'][0] === 'Points must be an integer number')
            message = createParagraph('Количество очков должно быть натуральным числом')
        if (data['errors'][0] === 'You are stockholder of this company')
            message = createParagraph('Вы не можете голосовать за компании, акционером которых Вы являетесь')
        if (data['errors'][0] === 'You do not have enough points') {
            points = data['data']['points']
            message = document.createElement('div')
            p1 = document.createElement('p')
            p1.textContent = "Недостаточно очков доверия"
            p2 = document.createElement('p')
            p2.textContent = "Свободных очков: " + points
            message.appendChild(p1)
            message.appendChild(p2)
        }
        showModal(message)
        votes.get()
        sectors = Object.keys(votes.getJson['votes'])

        for (sectorId = 0; sectorId < sectors.length; sectorId++) {
            for (companyId = 0; companyId < votes.getJson['votes'][sectors[sectorId]].length;
                 companyId++) {

                const companyTitle = votes.getJson['votes'][sectors[sectorId]][companyId]['company']
                document.getElementById(companyTitle).onclick = function () {
                    points = parseInt(document.getElementById('points').value)
                    votes.put(companyTitle, points, function (data) {
                        changeVotingValues(companyTitle, points, data)
                    })
                }

            }
        }

    }
}
