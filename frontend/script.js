const chatbox = document.querySelector('.chatbox');
const chatInput = document.querySelector('.chat-input textarea');
const sendBtn = document.getElementById('send-btn');

const createChatLi = (message, className) => {
    const chatLi = document.createElement('li');
    chatLi.classList.add('chat', className);
    chatLi.innerHTML = `<p>${message}</p>`;
    return chatLi;
}

const handleChat = () => {
    const userMessage = chatInput.value.trim();
    if (!userMessage) return;

    // Add user message
    chatbox.appendChild(createChatLi(userMessage, 'outgoing'));
    chatInput.value = '';
    
    // Get bot response from Flask
    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
    })
    .then(res => res.json())
    .then(data => {
        chatbox.appendChild(createChatLi(data.response, 'incoming'));
        chatbox.scrollTop = chatbox.scrollHeight;
    });
}

sendBtn.addEventListener('click', handleChat);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleChat();
    }
});
