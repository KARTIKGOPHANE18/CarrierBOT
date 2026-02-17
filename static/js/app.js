function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value;
    if (!message) return;

    appendMessage(message, "user");
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => appendMessage(data.reply, "bot"));
}

function appendMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

