// app.js

// Register the service worker (this part stays the same)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then(reg => console.log('Service Worker Registered', reg))
      .catch(err => console.error('Service Worker Error', err));
  });
}

// AI-powered chatbot functionality (append this code)
document.getElementById('send-btn').addEventListener('click', () => {
  const userInput = document.getElementById('user-input').value;
  if (userInput) {
    updateChat(userInput, 'user');
    fetchAIResponse(userInput);
    document.getElementById('user-input').value = '';
  }
});

function updateChat(message, sender) {
  const chatbox = document.getElementById('chatbox');
  const messageElem = document.createElement('div');
  messageElem.textContent = `${sender === 'user' ? 'You' : 'AI'}: ${message}`;
  chatbox.appendChild(messageElem);
  chatbox.scrollTop = chatbox.scrollHeight;
}

async function fetchAIResponse(query) {
  // Replace 'YOUR_API_KEY' with your actual key from an AI provider (e.g., OpenAI, etc.)
  const apiUrl = 'https://api.openai.com/v1/completions';
  
  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer YOUR_API_KEY`
    },
    body: JSON.stringify({
      model: 'text-davinci-003',
      prompt: query,
      max_tokens: 150
    })
  });
  
  const data = await response.json();
  const aiMessage = data.choices[0].text.trim();
  updateChat(aiMessage, 'ai');
}
