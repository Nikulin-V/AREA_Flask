/*
 * Nikulin Vasily © 2021
 */

updatePage()
html = document.getElementsByTagName('html')[0]
window.addEventListener('scroll', function () {
    let height = Math.max(document.body.scrollHeight, document.body.offsetHeight,
        html.clientHeight, html.scrollHeight, html.offsetHeight)
    if (pageYOffset + window.innerHeight + 1 >= height) {
        addNews(k, false)
    }
})

function updatePage(isFullUpdate = true) {
    k = 0
    was_end = false
    addNews(k, isFullUpdate)
}

main = document.getElementsByTagName('main')[0]

function addNews(page = 0, isFullUpdate = true) {
    if (!was_end)
        news.get(page, function (data) {
            if (data['news']) {
                if (isFullUpdate) {
                    main = document.getElementsByTagName('main')[0]
                    while (document.getElementsByClassName('news').length > 0)
                        main.removeChild(document.getElementsByClassName('news')[0])
                    document.getElementById('username').scrollIntoView()
                }

                const newsList = data['news']
                for (newsId = 0; newsId < newsList.length; newsId++) {
                    const n = Object(newsList[newsId])
                    if (n.picture)
                        picture = `<img id="${n.id}-picture" src="${n.picture}" alt="Неверная ссылка на изображение новости" class="rounded img-fluid mx-auto d-block">`
                    else
                        picture = ''
                    if (n.canEdit)
                        authorButtons = `
                                <div style="display: inline-flex">
                                    <button onclick="deleteNews('${n.id}')" class="btn btn-outline-danger btn-delete btn-icon"><span class="material-icons md-red">clear</span></button>
                                    <button onclick="editNews('${n.id}')" class="btn btn-outline-warning btn-edit btn-icon"><span class="material-icons-round md-yellow">edit</span></button>
                                </div>`
                    else authorButtons = ''
                    likes = parseInt(n.likes) > 0 ? " " + n.likes.toString() : ""
                    newsFooter = `
                        <table style="width: 100%; border: 0; margin: 5px 0">
                            <tr style="border: 0">
                                <td rowspan="2" style="text-align: left; border: 0; width: 1%">
                                    ${authorButtons}
                                </td>
                                <td style="border: 0">
                                    <p style="margin-bottom: 0;${isMobile() ? " font-size: .7em;" : ""} text-align: center">
                                        ${n.header_down}
                                    </p>
                                </td>
                                <td rowspan="2" style="text-align: right; border: 0; width: 1px">
                                    <button id="${n.id}-like" onclick="like('${n.id}')" class="btn btn-outline-danger btn-like btn-icon">
                                        <span id="${n.id}-like-symbol" class="material-icons-round md-red">favorite${n.isLiked ? "" : "_border"}</span>
                                        <span id="${n.id}-like-counter" class="btn-icon-text">${likes}</span>
                                    </button>
                                </td>
                            </tr>
                            <tr style="border: 0">
                                <td style="border: 0">
                                    <p style="margin-bottom: 0; font-size: .7em; text-align: center">${n.date}</p>
                                </td>
                            </tr>
                        </table>
                    `
                    main.innerHTML += `
                            <div class="news" id="${n.id}" style="border: 1px solid black; border-radius: 5px; margin-bottom: 5px; padding: 5px 5px 0 5px">
                                <table style="width: 100%; border: 0">
                                    <tr style="border: 0">
                                        <td rowspan="2" style="text-align: center; border: 0; word-wrap: anywhere">
                                            <h4 id="${n.id}-title">${n.title}</h4>
                                        </td>
                                    </tr>
                                </table>
                                <p id="${n.id}-text" style="word-break: break-all; white-space: pre-wrap">${n.message}</p>
                                ${picture}
                                ${newsFooter}
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
                <input id="title-input" class="form-control" placeholder="Заголовок" onclick="valid(this)" autocomplete="off">
                <label for="title-input">Заголовок</label>
            </div>
            <br>
            <div class="form-floating">
                <textarea id="text-input" class="form-control" placeholder="Текст"></textarea>
                <label for="text-input">Текст</label>
            </div>
            <br>
            <div class="mb-3">
                <label for="image-input">Изображение</label>
                <input type="file" id="image-input" name="illustration" class="form-control" placeholder="Изображение" accept="image/*"  onclick="valid(this)" autocomplete="off">
                <div class="invalid-feedback" id="image-feedback"></div>
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

    progressBarBack = document.createElement('div')
    progressBarBack.className = "progress"
    progressBar = document.createElement('div')
    progressBarBack.appendChild(progressBar)
    progressBar.className = "progress-bar progress-bar-striped progress-bar-animated btn-info"
    progressBar.setAttribute("role", "progressbar")
    progressBar.setAttribute("aria-valuemin", "0")
    progressBar.setAttribute("aria-valuemax", "0")
    progressBar.setAttribute("aria-valuenow", "0")
    progressBarBack.style.width = "100%"
    progressBar.style.width = "0%"
    progressBarBack.style.display = "none"


    button.onclick = function () {
        const title = document.getElementById('title-input').value
        if (title) {

            if (document.getElementById('image-input').files.length === 0) {
                const text = document.getElementById('text-input').value
                const author = document.getElementById('author-select')
                const authorValue = author.options[author.selectedIndex].value

                news.post(authorValue, title, text, null, null, updatePage)
                closeModal()
            } else {
                let image = document.getElementById('image-input').files[0]

                button.style.display = "none"
                progressBarBack.style.removeProperty("display")

                news.uploadImage(image, (progress) => {
                    progressBar.style.width = progress + "%"
                    progressBar.setAttribute("aria-valuemin", progress.toString())
                }, (data) => {
                    if (data["error"]) {
                        document.getElementById('image-input').classList.add('is-invalid')
                        if (data["code"] === 1001) {
                            document.getElementById('image-feedback').textContent = "Неверный или небезопасный формат файла"
                        }
                        progressBarBack.style.display = "none"
                        progressBar.style.width = "0%"
                        progressBar.setAttribute("aria-valuemin", "0")
                        button.style.removeProperty("display")
                    } else {
                        const text = document.getElementById('text-input').value
                        const imagePath = data["path"]
                        const jobId = data["jobId"]
                        const author = document.getElementById('author-select')
                        const authorValue = author.options[author.selectedIndex].value

                        news.post(authorValue, title, text, imagePath, jobId, updatePage)
                        closeModal()
                    }
                }, () => {
                    document.getElementById('image-input').classList.add('is-invalid')
                    document.getElementById('image-feedback').textContent = "Файл слишком большой, пожалуйста выберите файл менее 32МБ"
                    progressBarBack.style.display = "none"
                    progressBar.style.width = "0%"
                    progressBar.setAttribute("aria-valuemin", "0")
                    button.style.removeProperty("display")
                })

            }
        } else document.getElementById('title-input').classList.add('is-invalid')
    }
    fillAuthors()
    showModal(message, 'Новый пост', [button, progressBarBack])
}

function fillAuthors(selectedValue = null) {
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
    const imageElement = document.getElementById(id + "-picture")
    noImage = !imageElement
    message =
        `<div>
            <div class="form-floating">
                <input id="title-input" class="form-control" placeholder="Заголовок" value="${title}" onclick="valid(this)" autocomplete="off">
                <label for="title-input">Заголовок</label>
            </div>
            <br>
            <div class="form-floating">
                <textarea id="text-input" class="form-control" placeholder="Текст">${text}</textarea>
                <label for="text-input">Текст</label>
            </div>
            <br>
            <div class="mb-3">
                <label for="image-input">Изображение</label>
                <input type="file" id="image-input" name="illustration" class="form-control" placeholder="Изображение" accept="image/*" onclick="valid(this)" autocomplete="off">
                <div class="invalid-feedback" id="image-feedback"></div>
            </div>
            <br>
        </div>`
    button = document.createElement('button')
    button.textContent = "Сохранить"
    button.className = "btn btn-info"

    progressBarBack = document.createElement('div')
    progressBarBack.className = "progress"
    progressBar = document.createElement('div')
    progressBarBack.appendChild(progressBar)
    progressBar.className = "progress-bar progress-bar-striped progress-bar-animated btn-info"
    progressBar.setAttribute("role", "progressbar")
    progressBar.setAttribute("aria-valuemin", "0")
    progressBar.setAttribute("aria-valuemax", "0")
    progressBar.setAttribute("aria-valuenow", "0")
    progressBarBack.style.width = "100%"
    progressBar.style.width = "0%"
    progressBarBack.style.display = "none"

    btnClear = document.createElement("clear-image")
    btnClear.textContent = "Удалить изображение"
    btnClear.className = "btn btn-info"
    btnClear.onclick = () => {
        news.put(id, null, null, "!clear", null, null, updatePage)
        closeModal()
    }

    button.onclick = () => {
        const newTitle = document.getElementById('title-input').value

        if (newTitle) {
            const newText = document.getElementById('text-input').value
            if (document.getElementById('image-input').files.length === 0) {
                news.put(id, newTitle, newText, null, null, null, updatePage)
                closeModal()
            } else {
                let newImage = document.getElementById('image-input').files[0]

                button.style.display = "none"
                if (noImage) btnClear.style.display = "none"
                progressBarBack.style.removeProperty("display")

                news.uploadImage(newImage, (progress) => {
                    progressBar.style.width = progress + "%"
                    progressBar.setAttribute("aria-valuemin", progress.toString())
                }, (data) => {
                    if (data["error"]) {
                        document.getElementById('image-input').classList.add('is-invalid')
                        if (data["code"] === 1001) {
                            document.getElementById('image-feedback').textContent = "Неверный или небезопасный формат файла"
                        }
                        progressBarBack.style.display = "none"
                        progressBar.style.width = "0%"
                        progressBar.setAttribute("aria-valuemin", "0")
                        button.style.removeProperty("display")
                        if (noImage) btnClear.style.removeProperty("display")
                    } else {
                        const newImagePath = data["path"]
                        const jobId = data["jobId"]
                        news.put(id, newTitle, newText, newImagePath, null, jobId, updatePage)
                        closeModal()
                    }
                }, () => {
                    document.getElementById('image-input').classList.add('is-invalid')
                    document.getElementById('image-feedback').textContent = "Файл слишком большой, пожалуйста выберите файл менее 32МБ"
                    progressBarBack.style.display = "none"
                    progressBar.style.width = "0%"
                    progressBar.setAttribute("aria-valuemin", "0")
                    button.style.removeProperty("display")
                })
            }
        } else document.getElementById('title-input').classList.add('is-invalid')
    }
    showModal(message, 'Изменение поста', noImage ? [button, progressBarBack] : [btnClear, button, progressBarBack])
}

function deleteNews(id) {
    news.delete(id, function () {
        newsPost = document.getElementById(id)
        main.removeChild(newsPost)
    })
}

function like(id) {
    news.put(id, null, null, null, true, null, function (data) {
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

function valid(element) {
    if (element.classList.contains("is-invalid")) {
        element.classList.remove("is-invalid")
    }
}

function showNewPosts() {
    let newPostsBtn = document.getElementById('news-update-btn')
    updatePage();
    newPostsBtn.style.display = 'none';
    let usernameBtn = document.getElementById('username')
    usernameBtn.scrollIntoView()
}

function showNewPostsBtn() {
    document.getElementById('news-update-btn').style.display = "block"
}
