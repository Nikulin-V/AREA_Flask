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
                    authorButtons = `<button onclick="deleteNews('${ n.id }')" class="btn btn-outline-danger btn-delete">❌</button>
                                    <button onclick="editNews('${ n.id }')" class="btn btn-outline-warning btn-edit">✏</button>`
                else authorButtons = ''
                likes = parseInt(n.likes) > 0 ? " " + n.likes.toString() : ""
                main.innerHTML = main.innerHTML +
                `
                <div class="news" id="${ n.id }" style="border: 1px solid black; border-radius: 5px; margin-bottom: 5px; padding: 5px 5px 0 5px">
                    <table style="width: 100%; border: 0">
                        <tr style="border: 0">
                            <td rowspan="2" style="text-align: left; border: 0; word-wrap: anywhere">
                                <h4 id="${ n.id }-title">${ n.title }</h4>
                            </td>
                            <td style="text-align: right; border: 0">
                                <p style="margin-bottom: 0"><small>${ n.author }</small></p>
                            </td>
                        </tr>
                        <tr style="border: 0">
                            <td style="text-align: right; border: 0">
                                <p style="margin-bottom: 0"><small> ${ n.date }</small></p>
                            </td>
                        </tr>
                    </table>
                    <p id="${ n.id }-text" style="word-break: break-all; white-space: pre-wrap">${ n.message }</p>
                    ${ picture }
                    <table style="width: 100%; border: 0; margin: 5px 0">
                        <tr style="font-size: 1em; border: 0">
                            <td style="text-align: left; border: 0">
                                ${ authorButtons }
                            </td>
                            <td style="text-align: right; border: 0">
                                <button id="${ n.id }-like" onclick="like('${ n.id }')" class="btn btn-outline-danger btn-like">❤${ likes }</button>
                            </td>
                        </tr>
                    </table>
                </div>
                `
            }
        } else was_end = true
        k += 1
    })
}

function createNews() {
    message =
        `<div>
            <div class="form-floating">
                <input id="title-input" class="form-control" placeholder="Заголовок">
                <label for="title-input">Заголовок</label>
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
        likeButton = document.getElementById(id + '-like')
        if (data["likes"] === 0)
            likeButton.textContent = "❤"
        else likeButton.textContent = "❤ " + data["likes"].toString()
    })
}