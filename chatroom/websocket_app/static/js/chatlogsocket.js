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
      addChatlogMessage(JSON.parse(e.data), name)
    };
    window.chatSocket.onclose = function (e) {};
    window.chatSocket.addEventListener("open", (event) => {}); 
}
    
function addChatlogMessage(data, user) {
    last_message_block = document.querySelector("#chat-log").firstChild;
    
    if (last_message_block && last_message_block.id == data.user) {
      extendChatLogMessageBlock(last_message_block, data)
    } else {
      createChatLogMessageBlock(data, user)
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
    message_block.className += (data.is_author) ? "align-self-end justify-content-end" : "align-self-start justify-content-start";
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
    data.is_author ? message_block.append(message_block_picture) : message_block.prepend(message_block_picture);
    document.getElementById("chat-log").prepend(message_block);
    
}
    
    