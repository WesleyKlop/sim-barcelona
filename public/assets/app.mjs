const $log = document.querySelector('#log')
const $result = document.querySelector('#result')
const $loadingOverlay = document.querySelector('#loading-overlay')

const evtSource = new EventSource('/api/listen')

const clearLog = () => {
    $log.innerHTML = 'Log:\n'
}

const setImage = (url) => {
    $result.src = url
}

const setLoading = (isLoading) => {
    if (isLoading) {
        $loadingOverlay.classList.remove('hidden')
    } else {
        $loadingOverlay.classList.add('hidden')
    }
}

const BLANK_IMAGE = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='

evtSource.addEventListener('phase', ({data}) => {
    switch (data) {
        case 'running':
            clearLog()
            setLoading(true)
            setImage(BLANK_IMAGE)
            break
        case 'finished':
            setLoading(false)
            break
        case 'error':
            $log.classList.remove('hidden')
            setLoading(false)
            setImage(BLANK_IMAGE)
            break
    }
})

evtSource.addEventListener('image', ({data}) => {
    setImage(data)
})

evtSource.addEventListener('log', ({data}) => {
    $log.innerHTML += data.trim() + '\n'
})