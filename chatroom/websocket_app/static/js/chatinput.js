document.querySelector("#chat-message-input").focus();
document.querySelector("#chat-message-input").onkeyup = function (e) {
  if (e.keyCode === 13) {
    // enter, return
    document.querySelector("#chat-message-submit").click();
  }
};

document.querySelector("#chat-message-submit").onclick = function (e) {
var messageInputDom = document.querySelector("#chat-message-input");
var message = messageInputDom.value;
window.chatSocket.send(
  JSON.stringify({
    message: message,
  })
);
messageInputDom.value = "";
};


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
  newSocketChatlogConnection(this.id, this.name);
};  
document.querySelector('#chat-rooms').prepend(room)
};

function newSocketChatlogConnection(id, name) {
// закрываем старое соединение с групповым чатом
window.chatSocket?.close()
// чистим чат
document.querySelector("#chat-log").innerHTML = ""
// укащзываем имя в окне чата 
document.querySelector('#room-name').textContent = name;
// удаляем уведомления
document.querySelector(`#btn_${id}`)?.remove();

// создаем новое соединение с групопвым чатом
window.chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat-log/" + id + "/"
);
window.chatSocket.onmessage = function (e) {
  addChatlogMessage(JSON.parse(e.data))
};
window.chatSocket.onclose = function (e) {};
window.chatSocket.addEventListener("open", (event) => {}); 
}

function addChatlogMessage(data) {
last_message_block = document.querySelector("#chat-log").firstChild;

if (last_message_block && last_message_block.id == data.user) {
  extendChatLogMessageBlock(last_message_block, data)
} else {
  createChatLogMessageBlock(data)
};
};

function extendChatLogMessageBlock(target, data) {
target.querySelector("#chat-log-message-block").innerHTML += `
    <div class="d-flex flex-column m-2 rounded-2 bg-light shadow-sm">
      <div class="d-flex justify-content-between align-items-center">
        <div class="h6 m-0 p-2">${data.user}</div>
        <div class="text-muted p-2 fs-10">
          <small>${data.message_time}</small>
        </div>
      </div>
      <div class="p-2">${data.message_text}</div>
    </div>
  `
}

function createChatLogMessageBlock(data) {
let message_block = document.createElement("div")
message_block.className = "d-flex ";
message_block.className += (data.user === "{{ user }}") ? "align-self-end justify-content-end" : "align-self-start justify-content-start";
message_block.style = "width:fit-content; max-width: 75%;"
message_block.id = data.user

let message_block_message = document.createElement("div")
message_block_message.id = "chat-log-message-block"
message_block_message.className = "d-flex flex-column";


let message_block_picture = document.createElement("div")
message_block_picture.width = message_block_picture.height = 40 

message_block_picture.className = "align-self-end m-2";
if (data.profile_picture) {
  message_block_picture.innerHTML =  `<div class="btn btn-primary rounded rounded-circle p-0" style="height:40px; width:40px;"><img class="img-fluid rounded rounded-circle m-0 p-0" style="width: 100%; height: 100%; object-fit: cover;" src="/images/profile_pic/user_2.png"></div>`
} else {
  message_block_picture.innerHTML = `<div class="btn btn-primary rounded rounded-circle">${data.user[0].toUpperCase()}</div>`
}

let message = document.createElement("div")
message.innerHTML = `
  <div class="d-flex flex-column m-2 rounded-2 bg-light shadow-sm">
    <div class="d-flex justify-content-between align-items-center">
      <div class="h6 m-0 p-2">${data.user}</div>
      <div class="text-muted p-2 fs-10"><small>${data.message_time}</small></div>
    </div>
    <div class="p-2">${data.message_text}</div>
  </div>
`; 
    
message_block_message.append(message)
message_block.append(message_block_message)
data.user == "{{ user }}"  ? message_block.append(message_block_picture) : message_block.prepend(message_block_picture);
document.querySelector("#chat-log").prepend(message_block);

}

