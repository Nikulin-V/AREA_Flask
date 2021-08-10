/*
 * Nikulin Vasily © 2021
 */

updatePage()
html = document.getElementsByTagName('html')[0]
window.addEventListener('scroll', function() {
    let height = Math.max(document.body.scrollHeight, document.body.offsetHeight,
                          html.clientHeight, html.scrollHeight, html.offsetHeight)
    if (pageYOffset + window.innerHeight + 1 >= height) {
        addNews(k)
    }
})

function updatePage() {
    main = document.getElementsByTagName('main')[0]
    while (document.getElementsByClassName('news').length > 0)
        main.removeChild(document.getElementsByClassName('news')[0])
    k = 0
    was_end = false
    addNews(k)
}

main = document.getElementsByTagName('main')[0]
function addNews(page=0) {
    if (!was_end)
    news.get(page, function (data) {
        if (data['news']) {
            newsList = data['news']
            for (newsId = 0; newsId < newsList.length; newsId++) {
                n = Object(newsList[newsId])
                if (n.picture)
                    picture = `<img id="${ n.id }-picture" src="${ n.picture }" alt="Неверная ссылка на изображение новости" class="rounded img-fluid mx-auto d-block">`
                else
                    picture = ''
                if (n.canEdit)
                    authorButtons = `
                                    <div style="display: inline-flex">
                                    <button onclick="deleteNews('${ n.id }')" class="btn btn-outline-danger btn-delete btn-icon"><span class="material-icons md-red">clear</span></button>
                                    <button onclick="editNews('${ n.id }')" class="btn btn-outline-warning btn-edit btn-icon"><span class="material-icons-round md-yellow">edit</span></button>
                                    </div>`
                else authorButtons = ''
                if (n.author.split('|').length === 2)
                    author = n.author.split(' | ')[0] + '<br>' + n.author.split(' | ')[1]
                else
                    author = n.author
                likes = parseInt(n.likes) > 0 ? " " + n.likes.toString() : ""
                icon = n.is_liked ? "/static/images/icons/like_fill.svg" : "/static/images/icons/like_hollow.svg"
                main.innerHTML = main.innerHTML +
                `
                <div class="news" id="${ n.id }" style="border: 1px solid black; border-radius: 5px; margin-bottom: 5px; padding: 5px 5px 0 5px">
                    <h6 id="${ n.id }-title" style="word-wrap: anywhere">${ n.title }</h6>
                    <p id="${ n.id }-text" style="word-break: break-all; white-space: pre-wrap; font-size: .7em">${ n.message }</p>
                    ${ picture }
                    <table style="width: 100%; border: 0; margin: 5px 0">
                        <tr style="border: 0">
                            <td rowspan="2" style="text-align: left; border: 0; width: 1%">
                                ${ authorButtons }
                            </td>
                            <td style="border: 0">
                                <p style="margin-bottom: 0; font-size: .7em; text-align: center">
                                    ${ author }
                                </p>
                            </td>
                            <td rowspan="2" style="text-align: right; border: 0; width: 1px">
                                <button id="${ n.id }-like" onclick="like('${ n.id }')" class="btn btn-outline-danger btn-like btn-icon">
                                    <span id="${ n.id }-like-symbol" class="material-icons-round md-red">favorite${ n.isLiked ? "" : "_border" }</span>
                                    <span id="${ n.id }-like-counter" class="btn-icon-text">${ likes }</span>
                                </button>
                            </td>
                        </tr>
                        <tr style="border: 0">
                            <td style="border: 0">
                                <p style="margin-bottom: 0; font-size: .7em; text-align: center">${ n.date }</p>
                            </td>
                        </tr>
                    </table>
                </div>
                `
            }
        } else {
            was_end = true
            if (k === 0)
                main.insertAdjacentHTML('beforeend',
                    `
                        <table class="dairy-table table-hover table-info">
                            <tr style="background-color: #86CFDA">
                                <td style="text-align: center;padding: 5px">Новостей нет</td>
                            </tr>
                        </table>
                    `)
        }
        k += 1
    })
}

function createNews() {
    message =
        `<div>
            <div class="form-floating">
                <input id="title-input" class="form-control" placeholder="Заголовок">
                <label for="title-input">Заголовок</label>
                <div class="invalid-feedback">
                    Необходимо указать заголовок
                </div>
            </div>
            <br>
            <div class="form-floating">
                <textarea id="text-input" class="form-control" placeholder="Текст"></textarea>
                <label for="text-input">Текст</label>
            </div>
            <br>
            <div class="form-floating">
                <input id="image-input" class="form-control" placeholder="Ссылка на изображение">
                <label for="image-input">Ссылка на изображение</label>
            </div>
            <br>
            <div class="form-floating">
                <select id="author-select" class="form-select">
                    <option>от себя</option>
                </select>
                <label for="author-select">Подпись</label>
            </div>
        </div>`
    button = document.createElement('button')
    button.textContent = "Опубликовать"
    button.className = "btn btn-info"
    button.onclick = function () {
        const title = document.getElementById('title-input').value
        const text = document.getElementById('text-input').value
        const imageUrl = document.getElementById('image-input').value
        const author = document.getElementById('author-select')
        const authorValue = author.options[author.selectedIndex].value
        if (title) {
            news.post(authorValue, title, text, imageUrl, updatePage)
            closeModal()
        } else document.getElementById('title-input').classList.add('is-invalid')
    }
    fillAuthors()
    showModal(message, 'Новый пост', [button])
}

function fillAuthors (selectedValue=null) {
    stocks.get(
        function () {
            stocksJson = stocks.getJson['stocks']
            for (companyId = 0; companyId < stocksJson.length; companyId++) {
                companyTitle = stocksJson[companyId]['company']
                if (selectedValue === companyTitle)
                    selectedIndex = companyId
                $("#author-select").append(new Option('от лица компании "' + companyTitle + '"',
                    companyTitle))
            }
            if (selectedValue)
                document.getElementById('authors-select').selectedIndex = selectedIndex
        }
    )
}

function editNews(id) {
    id = id.toString()
    const titleElement = document.getElementById(id + "-title")
    title = titleElement.textContent
    const textElement = document.getElementById(id + "-text")
    if (textElement)
        text = textElement ? textElement.textContent : ''
    const imageUrlElement = document.getElementById(id + "-picture")
    imageUrl = imageUrlElement ? imageUrlElement.src : ''
    message =
        `<div>
            <div class="form-floating">
                <input id="title-input" class="form-control" placeholder="Заголовок" value="${ title }">
                <label for="title-input">Заголовок</label>
                <div class="invalid-feedback">
                    Необходимо указать заголовок
                </div>
            </div>
            <br>
            <div class="form-floating">
                <textarea id="text-input" class="form-control" placeholder="Текст">${ text }</textarea>
                <label for="text-input">Текст</label>
            </div>
            <br>
            <div class="form-floating">
                <input id="image-input" class="form-control" placeholder="Ссылка на изображение" value="${ imageUrl }">
                <label for="image-input">Ссылка на изображение</label>
            </div>
            <br>
        </div>`
    button = document.createElement('button')
    button.textContent = "Сохранить"
    button.className = "btn btn-info"
    button.onclick = function () {
        const newTitle = document.getElementById('title-input').value
        const newText = document.getElementById('text-input').value
        const newImageUrl = document.getElementById('image-input').value
        if (title) {
            news.put(id, newTitle, newText, newImageUrl, null, updatePage)
            closeModal()
        } else document.getElementById('title-input').classList.add('is-invalid')

    }
    showModal(message, 'Изменение поста', [button])
}

function deleteNews(id) {
    news.delete(id, function () {
        newsPost = document.getElementById(id)
        main.removeChild(newsPost)
    })
}

function like(id) {
    news.put(id, null, null, null, true, function (data) {
        let likeSymbol = document.getElementById(id + "-like-symbol")
        let likeCounter = document.getElementById(id + "-like-counter")

        if (data["isLiked"]) {
            likeSymbol.textContent = "favorite"
        } else {
            likeSymbol.textContent = "favorite_border"
        }

        if (data["likes"] === 0) {
            likeCounter.textContent = ""
        } else {
            likeCounter.textContent = data["likes"].toString()
        }
    })
}
