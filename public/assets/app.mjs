const evtSource = new EventSource('/api/listen')

const $log = document.querySelector('#log')

evtSource.addEventListener('message', (evt) => {
    alert('Got data!')
    document.write(evt.data)
})

evtSource.addEventListener('result', ({data}) => {
    const image = new Image()
    image.src = data
    document.body.appendChild(image)
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
