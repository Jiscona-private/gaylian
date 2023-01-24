function open(websocket) {
    document.getElementById('open').addEventListener("click", ({ target }) => {
        const token = document.getElementById('roomToken').value;
        const username = document.getElementById('username').value;
        localStorage.setItem('token', token);
        localStorage.setItem('username', username);
        window.location.href = 'chatInterface.html';
    })
    
}

window.addEventListener("DOMContentLoaded", () => {
    // Open the WebSocket connection and register event handlers.
    const websocket = new WebSocket("ws://localhost:7125/");
    print("OPENING")
    open(websocket)
});

