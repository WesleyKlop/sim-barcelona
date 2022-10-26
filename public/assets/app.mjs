
const evtSource = new EventSource('/api/listen')
evtSource.addEventListener('message', (evt) => {
    alert('Got data!')
    document.write(evt.data)
})

evtSource.addEventListener('error', async (evt) => {
    console.log('')
    console.error(evt)
    await new Promise(res => setTimeout(res, 5000))
    location.reload()
})
