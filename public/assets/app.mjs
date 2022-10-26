alert('Page loaded')

const evtSource = new EventSource('/api/listen')
evtSource.addEventListener('message', (evt) => {
    alert('Got data!')
    document.write(evt.data)
})

evtSource.addEventListener('error', (evt) => {
    alert(`error: ${evt}`)
})
