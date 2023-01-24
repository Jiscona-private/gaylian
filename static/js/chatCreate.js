function create(websocket) {
    document.getElementById('create').addEventListener("click", ({ target }) => {
        const token = document.getElementById('roomToken').value;
        const username = document.getElementById('username').value;
        localStorage.setItem('token', token);
        localStorage.setItem('username', username);
        // sending init msg
        const event = {
            type: "create",
            token: token,
            username: username,
        };
        websocket.send(JSON.stringify(event));
        window.location.href = 'index.html';
    })
    
}

window.addEventListener("DOMContentLoaded", () => {
    // Open the WebSocket connection and register event handlers.
    const websocket = new WebSocket("ws://localhost:7125/");
    create(websocket)
});

