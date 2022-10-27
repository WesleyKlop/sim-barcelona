const evtSource = new EventSource('/api/listen')

const $log = document.querySelector('#log')
const $before = document.querySelector('#before')
const $result = document.querySelector('#result')
const $main = document.documentElement;

evtSource.addEventListener('message', (evt) => {
    console.log("message")
    alert('Got data!')
    document.write(evt.data)
})

evtSource.addEventListener('start', ({data}) => {
    console.log("start")
    $log.innerHTML = 'Log:\n'
    $before.src = data
    if (document.getElementById("loading-div") != null) 
    {
        return;
    }
    $main.innerHTML += `
    <div id="loading-div" class="loading-div" style=" 
        position: absolute;
        left: 0;
        top: 0;
        background-color: rgba(1, 1, 1, 0.2);
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-content: center;
    ">
        <text class="loading-text" style="    
            font-size: 15em;
            color: white;
            text-shadow: 0 0 20px #000;    
        ">
            loading...</text>
    </div>`
})

evtSource.addEventListener('result', ({data}) => {
    console.log("result")
    $result.src = data
    const loadingDiv = document.getElementById("loading-div")
    console.log(loadingDiv)
    let bodyElement = [].filter.call($main.childNodes, el => el.tagName == "BODY")[0]
    bodyElement.removeChild(loadingDiv)

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
