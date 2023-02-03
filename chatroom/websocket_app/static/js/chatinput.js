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
    user: "{{ user }}",
  })
);
messageInputDom.value = "";
};
