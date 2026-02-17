function addMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");

    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    msg.innerText = text;

    chatBox.appendChild(msg);

    // ✅ smooth auto-scroll
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: "smooth"
    });
}

function showTyping() {
    const chatBox = document.getElementById("chat-box");

    const typing = document.createElement("div");
    typing.className = "message bot typing";
    typing.id = "typing";
    typing.innerText = "CareerBot is typing...";

    chatBox.appendChild(typing);

    // smooth scroll
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: "smooth"
    });
}

function removeTyping() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
}

function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    showTyping();

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        removeTyping();
        addMessage(data.reply, "bot");
    });
}

/* ✅ 1️⃣ Enter key support */
document.getElementById("user-input").addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

