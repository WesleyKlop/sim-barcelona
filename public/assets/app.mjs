const evtSource = new EventSource('/api/listen')

const $log = document.querySelector('#log')
const $before = document.querySelector('#before')
const $result = document.querySelector('#result')

evtSource.addEventListener('message', (evt) => {
    alert('Got data!')
    document.write(evt.data)
})

evtSource.addEventListener('start', ({data}) => {
    $log.innerHTML = 'Log:\n'
    $before.src = data
})

evtSource.addEventListener('result', ({data}) => {
    $result.src = data
})

evtSource.addEventListener('log', ({data}) => {
    $log.innerHTML += data + '\n'
})

evtSource.addEventListener('error', async (evt) => {
    console.log('')
    console.error(evt)
    await new Promise(res => setTimeout(res, 5000))
    location.reload()
})
