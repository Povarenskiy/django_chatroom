window.roomSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat-rooms/" 
);
  
window.roomSocket.onmessage = function (e) {
  data = JSON.parse(e.data)
  document.getElementById(data.room_id)?.remove()
  addChatRoomRoom(data);
  document.getElementById('chatroom-count').innerHTML = `Комнат (${document.getElementById('chat-rooms').childElementCount})`;
}
  
window.roomSocket.onclose = function (e) {};
window.roomSocket.addEventListener("open", (event) => {}); 

  
function addChatRoomRoom(data) {
  let room = document.createElement("div");
  room.id = data.room_id
  room.name = data.room_name
  room.className = "btn btn-light shadow-sm rounded-0 room-btn border-top";
  room.innerHTML = `
  <div class="row justify-content-around">
    <div class="col">
      <div class="d-flex flex-column align-items-start">
        <div class="h6">${data.room_name}</div>
        <div class="text-center text-dark">${data.last_message}</div>
      </div>
    </div>
    <div class="col-3">
      <div class="d-flex flex-column text-center">
      <div class="align-self-start text-muted m-auto">${data.last_update}</div>
    ${data.notification ? (
        `<div class="text-primary" id="btn_${data.room_id}">*${data.notification}</div>
      </div>
    </div>`)
      : ''}
    </div>`;  
  
  room.onclick = function (e) {
    newSocketChatlogConnection(room.id, room.name);
  };  
  document.querySelector('#chat-rooms').prepend(room)
};
  