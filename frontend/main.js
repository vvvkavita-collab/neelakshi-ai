// frontend/main.js
const chatbox = document.getElementById('chatbox');
const messageInput = document.getElementById('message');
const sendBtn = document.getElementById('sendBtn');

// Deploy के बाद यह URL बदलना होगा
const BACKEND_URL = "https://neelakshi-ai-backend.onrender.com/chat";

function appendMessage(text, cls) {
  const d = document.createElement('div');
  d.className = 'msg ' + cls;
  d.textContent = text;
  chatbox.appendChild(d);
  chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage() {
  const text = messageInput.value.trim();
  if (!text) return;
  appendMessage("You: " + text, "user");
  messageInput.value = "";
  appendMessage("Neelakshi AI: Typing...", "bot");

  try {
    const res = await fetch(BACKEND_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    // remove the "Typing..." message
    const last = Array.from(chatbox.querySelectorAll('.bot')).pop();
    if (last && last.textContent.includes("Typing")) last.remove();

    appendMessage("Neelakshi AI: " + (data.reply || "Kuch galat ho gaya."), "bot");
  } catch (e) {
    const last = Array.from(chatbox.querySelectorAll('.bot')).pop();
    if (last && last.textContent.includes("Typing")) last.remove();
    appendMessage("Neelakshi AI: Server error - " + e.message, "bot");
  }
}

sendBtn.onclick = sendMessage;
messageInput.addEventListener('keypress', function(e){
  if (e.key === 'Enter') sendMessage();
});

