const evtSource = new EventSource('/api/listen')

const $log = document.querySelector('#log')
const $result = document.querySelector('#result')
const $loadingOverlay = document.querySelector('#loading-overlay')

let phase = 'finished'

const clearLog = () => {
    $log.innerHTML = 'Log:\n'
}

const setImage = (url) => {
    $result.src = url
}

const setLoading = (isLoading) => {
    if(isLoading) {
        $loadingOverlay.classList.remove('hidden')
    } else {
        $loadingOverlay.classList.add('hidden')
    }
}

evtSource.addEventListener('phase', ({data}) => {
    console.log('New phase', data)
    phase = data

    switch(data) {
        case 'running':
            clearLog()
            setLoading(true)
            break
        case 'finished':
            setLoading(false)
            break
    }
})

evtSource.addEventListener('image', ({data}) => {
    if(phase !== 'running')
    setImage(data)
})

evtSource.addEventListener('log', ({data}) => {
    $log.innerHTML += data + '\n'
})

evtSource.addEventListener('error', async (evt) => {
    $log.classList.remove('hidden')
    $log.innerHTML += evt.data
    // Sleep 10s and reload the page
    await new Promise(res => setTimeout(res, 10000))
    location.reload()
})
