function updateProgressbar(element, progress) {
    $(element).find('.video-download-init').css('opacity', '0')
    $(element).find('.video-progress-bar').css('width', progress+'%')

    if (progress != 0)
        $(element).find('.video-progress-bar>p').text(progress+'%')
    else
        $(element).find('.video-progress-bar>p').text('')

    if (progress == 100)
        window.setTimeout(() => updateProgressbar(element, 0), 100)
}

function downloadVideo(element, id, onlyAudio = false) {
    $(element).find('.video-download-init').css('opacity', '1')
    const title = $(element).find('.video-title').text()

    const xhr = new XMLHttpRequest()
    xhr.responseType = "blob"
    xhr.open('GET', `/download/${id}` + (onlyAudio ? '?audio' : ''), true)
    xhr.onprogress = ev => updateProgressbar($(element)[0], Math.ceil(ev.loaded / ev.total * 100))
    xhr.onloadend = async() =>  {
        if (xhr.status == 200)
            beginFileDownload(xhr.response, title + (onlyAudio ? '.mp3' : '.mp4'))
        else {
            const msg = await new Response(xhr.response).text()
            bs_alert(msg, 'danger')
        }
    }
    xhr.send(null)
}