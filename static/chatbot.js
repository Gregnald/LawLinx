const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const loader = document.getElementById("loader");

const sendMessage = async () => {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  userInput.value = "";
  loader.classList.remove("hidden");

  try {
    const response = await fetch("/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: message }),
    });

    const data = await response.json();
    appendMessage("bot", data.reply || "⚠️ No response.");
  } catch (err) {
    appendMessage("bot", "⚠️ Internal error. Try again.");
  }

  loader.classList.add("hidden");
};

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});

function appendMessage(sender, text) {
  const wrapper = document.createElement("div");
  wrapper.className = `message-wrapper ${sender}`;

  const msgDiv = document.createElement("div");
  msgDiv.className = `chat-message ${sender}`;
  msgDiv.innerText = text;

  wrapper.appendChild(msgDiv);
  chatBox.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
}
