const status = document.getElementById('status');
const responseText = document.getElementById('response');
const audioPlayer = document.getElementById('audio');

function startRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
        status.textContent = "🎤 Listening...";
    };

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        status.textContent = `📝 Heard: "${text}"`;
        sendText(text);
    };

    recognition.onerror = (event) => {
        status.textContent = `❌ Error: ${event.error}`;
    };

    recognition.start();
}

function sendText(text) {
    fetch('https://ubiquitous-octo-carnival-backend.onrender.com/process_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text }),
        mode: 'cors'
    })
    .then(response => response.json())
    .then(data => {
        responseText.textContent = "🤖 " + data.reply;
        if (data.audio_url) {
            audioPlayer.src = data.audio_url;
            audioPlayer.hidden = false;
            audioPlayer.play().catch(err => {
                console.warn("Audio playback failed:", err);
            });
        } else {
            console.warn("No audio URL returned.");
        }
    })
    .catch(error => {
        console.error("Full fetch error:", error);
        responseText.textContent = "❌ Failed to get response. See console for details.";
    });
}
