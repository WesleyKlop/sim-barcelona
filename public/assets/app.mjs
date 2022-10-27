const evtSource = new EventSource('/api/listen')

const $log = document.querySelector('#log')
const $before = document.querySelector('#before')
const $result = document.querySelector('#result')
const $loadingOverlay = document.querySelector('#loading-overlay')
const $main = document.documentElement;

evtSource.addEventListener('start', ({data}) => {
    console.log("start")
    $log.innerHTML = 'Log:\n'
    $before.src = data

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
    console.log('')
    console.error(evt)
    // Sleep 5s and reload the page
    await new Promise(res => setTimeout(res, 5000))
    location.reload()
})
