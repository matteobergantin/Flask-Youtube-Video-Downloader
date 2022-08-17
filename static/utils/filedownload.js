function beginFileDownload(blob, filename) {
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.setAttribute('download', filename)
    a.click()
    window.setTimeout(() => URL.revokeObjectURL(url), 100)
}