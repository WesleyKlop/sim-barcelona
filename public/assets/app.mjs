const evtSource = new EventSource('/api/listen')

const $log = document.querySelector('#log')
const $result = document.querySelector('#result')
const $loadingOverlay = document.querySelector('#loading-overlay')
const $main = document.documentElement;

evtSource.addEventListener('start', ({data}) => {
    console.log("start")
    $log.innerHTML = 'Log:\n'
    $result.src = data

    $loadingOverlay.classList.remove('hidden')
})

evtSource.addEventListener('result', ({data}) => {
    console.log("result")
    $result.src = data

    $loadingOverlay.classList.add('hidden')
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
