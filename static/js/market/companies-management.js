/*
 * Nikulin Vasily © 2021
 */

renderPage()

function renderPage() {
    svotes.get(createTable)
    companies.get()
}


function createTable() {

    let main = document.getElementsByTagName('main')[0]
    votingsTable = document.getElementsByClassName('votings-table')
    while (votingsTable.length > 0) {
        main.removeChild(votingsTable[0])
    }

    if (svotes.getJson["votes"].length > 0) {

        const table = main.appendChild(document.createElement('table'));
        table.className = "dairy-table table-hover table-info votings-table"
        if (window.isMobile)
            table.style.fontSize = ".7em"
        const caption = table.appendChild(document.createElement('caption'))
        caption.textContent = _('Голосования акционеров')
        caption.style.captionSide = "top"
        const thead = table.appendChild(document.createElement('thead'));
        thead.style.backgroundColor = "#86CFDA"
        const tr = thead.appendChild(document.createElement('tr'));

        let votesJson = svotes.getJson["votes"]
        tableData = []
        for (i = 0; i < votesJson.length; i++) {
            v = votesJson[i]
            if (v["is_voted"] === true)
                v["is_voted"] = '<span class="material-icons md-green" style="vertical-align: middle">check_circle</span>'
            else v["is_voted"] = '<span class="material-icons md-red" style="vertical-align: middle">cancel</span>'
            // noinspection JSNonASCIINames
            tableData.push(
                {
                    votingIdWord: v["id"],
                    companyWord: v["company"],
                    actionWord: v["action"],
                    votesWord: v["votes"],
                    yourChoice: v["is_voted"]
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
                svotes.put(values[0], function (data) {
                    changeVotingValues(values[0], data)
                })
            }

            values.forEach(value => {
                const td = tr.appendChild(document.createElement('td'))
                td.innerHTML = value.toString();
                td.style.textAlign = 'center'
            });
        });
    } else {
        while (document.getElementsByClassName('votings-table').length > 0)
            main.removeChild(document.getElementsByClassName('votings-table')[0])

        main.insertAdjacentHTML('beforeend', `
        <table class="dairy-table table-hover table-info votings-table">
            <tr style="background-color: #86CFDA">
                <td style="text-align: center;padding: 5px">${noOpenedVotingsWord}</td>
            </tr>
        </table>
        `)
    }
}

function changeVotingValues(votingId, data) {
    tr = document.getElementById(votingId)
    if (data['message'] === 'Success' && !data['data']['end']) {
        const tdVotes = tr.children[3]
        const tdDecision = tr.children[4]

        tdVotesArray = tdVotes.textContent.split('/')
        a = parseInt(tdVotesArray[0])

        if (tdDecision.innerHTML === '<span class="material-icons md-green" style="vertical-align: middle">check_circle</span>') {
            tdDecision.innerHTML = '<span class="material-icons md-red" style="vertical-align: middle;">cancel</span>'
            tdVotesArray[0] = (a - 1).toString()
        } else {
            tdDecision.innerHTML = '<span class="material-icons md-green" style="vertical-align: middle">check_circle</span>'
            tdVotesArray[0] = (a + 1).toString()
        }
        tdVotes.textContent = tdVotesArray.join('/')
    }
    if (data['message'] === 'Success' && data['data']['end']) {
        table = document.getElementsByClassName('votings-table')[0]
        tbody = table.getElementsByTagName('tbody')[0]
        if (tbody.children.length > 1)
            tbody.removeChild(tr)
        else {
            main = document.getElementsByTagName('main')[0]
            main.removeChild(table)
            main.insertAdjacentHTML('beforeend', `
                                            <table class="dairy-table table-hover table-info votings-table">
                                                <tr  style="background-color: #86CFDA">
                                                    <td style="text-align: center;padding: 5px">${noOpenedVotingsWord}</td>
                                                </tr>
                                            </table>
                                        `)
        }
    }
}

function createVotingAction() {
    companySelect = document.getElementById('companies-select')
    companyTitle = companySelect.options[companySelect.selectedIndex].value
    actionSelect = document.getElementById('actions-select')
    action = actionSelect.options[actionSelect.selectedIndex].value
    count = document.getElementById('stocks-input')
    if (count) {
        count = count.value
    }
    svotes.post(action, companyTitle, count, closeModalAndRenderPage)
    setTimeout(fillCompanies, 300)
}

function createVoting() {
    createVotingButton = document.createElement('button')
    createVotingButton.className = "btn btn-info"
    createVotingButton.onclick = function () {
        createVotingAction()
    }
    createVotingButton.textContent = _('Создать голосование')


    if (stocks.getJson['stocks'].length > 0) {
        showModal(getVotingElement(), _('Начать голосование'), [createVotingButton]);
        $('#actions-select').bind('change', function () {
            if (document.getElementById('actions-select').selectedIndex === 0)
                document.getElementById('stocks-count').style.display = "block"
            else
                document.getElementById('stocks-count').style.display = "none"
        })
        companies.get(fillCompanies)
    } else
        showModal(createParagraph('Вы не являетесь акционером компаний'))
}

function getVotingElement() {
    createVotingDiv = document.createElement('div')

    companiesDiv = document.createElement('div')
    companiesDiv.className = "form-floating"

    companiesSelect = document.createElement('select')
    companiesSelect.className = "form-select"
    companiesSelect.id = "companies-select"

    companiesLabel = document.createElement('label')
    companiesLabel.htmlFor = "companies-select"
    companiesLabel.textContent = _("Компания")

    companiesDiv.appendChild(companiesSelect)
    companiesDiv.appendChild(companiesLabel)

    createVotingDiv.appendChild(companiesDiv)

    br1 = document.createElement('br')
    createVotingDiv.appendChild(br1)

    actionsDiv = document.createElement('div')
    actionsDiv.className = "form-floating"

    actionsSelect = document.createElement('select')
    actionsSelect.className = "form-select"
    actionsSelect.id = "actions-select"

    option1 = document.createElement('option')
    option1.value = "releaseNewStocks"
    option1.textContent = _("Выпустить новые акции")
    actionsSelect.appendChild(option1)

    option2 = document.createElement('option')
    option2.value = "closeCompany"
    option2.textContent = _("Закрыть компанию")
    actionsSelect.appendChild(option2)
    actionsDiv.appendChild(actionsSelect)

    actionsLabel = document.createElement('label')
    actionsLabel.htmlFor = "actions-select"
    actionsLabel.textContent = _("Действие")
    actionsDiv.appendChild(actionsLabel)

    createVotingDiv.appendChild(actionsDiv)

    stocksDiv = document.createElement('div')
    stocksDiv.id = "stocks-count"

    br2 = document.createElement('br')
    stocksDiv.appendChild(br2)

    stocksCountDiv = document.createElement('div')
    stocksCountDiv.className = "form-floating"

    stocksInput = document.createElement('input')
    stocksInput.className = "form-control"
    stocksInput.id = "stocks-input"
    stocksInput.value = "1"
    stocksInput.min = "1"
    stocksInput.type = "number"

    stocksCountDiv.appendChild(stocksInput)

    stocksLabel = document.createElement('label')
    stocksLabel.htmlFor = "stocks-input"
    stocksLabel.textContent = _("Количество новых акций на 1 старую")

    stocksCountDiv.appendChild(stocksLabel)

    stocksDiv.appendChild(stocksCountDiv)

    createVotingDiv.appendChild(stocksDiv)

    return createVotingDiv
}
