var running = false
var msg = ""
var msg_user = document.getElementById("message").value
var socket = io.connect(location.protocol+'//' + document.domain + ':' + location.port);
socket.on('connect', function () {
    socket.emit('my event', {
        data: 'User Connected'
    })
})
$('form').on('submit', function (e) {
    e.preventDefault()
    let user_input = $('input.input-message').val()
    socket.emit('my event', {
        message: user_input
    })
    var div = document.createElement("div");
    div.innerHTML = "<span style='flex-grow:1'></span><div class='chat-message'>" + String(document.getElementById("message").value) + "</div>"
    div.className = "chat-message-div"
    document.getElementById("message-box").appendChild(div)
    $('input.input-message').val('').focus()
})
function send() {
    if (running == true)
    {
        return
    }
    running = true
}
socket.on('my response', function (msg) {
    console.log(msg)
    if (typeof msg.message !== 'undefined') {
        $('h3').remove()
    }
    msg = msg.message;
    var div = document.createElement("div");
    div.innerHTML = "<div class='chat-message'>" + String(msg) + "</div>"
    div.className = "chat-message-div"
    document.getElementById("message-box").appendChild(div)
    msg = ""
    running = false
})
