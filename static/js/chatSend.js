const msgField = document.getElementById('msg')
let messages = []


function receive( websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    messages.push(event)
    console.log(messages)
  });
}


function send(websocket) {
  // When clicking a column, send a "play" event for a move in that column.
  document.getElementById('send').addEventListener("click", ({ target }) => {
    const event = {
      type: "msg",
      token: localStorage.getItem('token'),
      msg: msgField.value,
    };
    websocket.send(JSON.stringify(event));
  });
}


window.addEventListener("DOMContentLoaded", () => {
  // Open the WebSocket connection and register event handlers.
  const websocket = new WebSocket("ws://localhost:7125/");
  receive(websocket);
  send(websocket);
});