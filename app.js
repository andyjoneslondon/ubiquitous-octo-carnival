const recordButton = document.getElementById('recordButton');
const responseText = document.getElementById('response');
const transcriptText = document.getElementById('transcript');
const spinner = document.getElementById('spinner');
const audioPlayer = document.getElementById('audio');
const playReplyButton = document.getElementById('playReply');

let mediaRecorder;
let chunks = [];

recordButton.addEventListener('click', async () => {
  // 🔓 Unlock mobile autoplay policies
  const unlockAudio = new Audio('data:audio/mp3;base64,//uQxAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAACcQCA...');
  unlockAudio.play().catch(() => {});

  // 📦 Preload the actual audio element (in case autoplay becomes allowed)
  audioPlayer.load();
  audioPlayer.play().catch(() => {}); // harmless if no src yet

  // UI reset
  responseText.textContent = '';
  transcriptText.textContent = '';
  audioPlayer.style.display = 'none';
  playReplyButton.style.display = 'none';

  recordButton.classList.add('disabled');
  spinner.style.display = 'block';

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    chunks = [];

    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('audio', blob, 'input.webm');

      try {
        const response = await fetch('https://ubiquitous-octo-carnival-backend.onrender.com/process_audio', {
          method: 'POST',
          body: formData
        });

        const result = await response.json();

        spinner.style.display = 'none';
        recordButton.classList.remove('disabled');

        if (result.transcript) {
          transcriptText.textContent = `📝 I Heard: "${result.transcript}"`;
        }

        if (result.reply) {
          responseText.textContent = `🤖 ${result.reply}`;
        }

        if (result.audio_url) {
          audioPlayer.src = result.audio_url;
          audioPlayer.style.display = 'block';

          try {
            await audioPlayer.play();
          } catch (err) {
            console.warn('Autoplay blocked, showing manual play button.', err);
            playReplyButton.style.display = 'inline-block';

            // Attach manual play trigger
            playReplyButton.onclick = async () => {
              try {
                await audioPlayer.play();
                playReplyButton.style.display = 'none';
              } catch (err) {
                console.error('Manual playback failed:', err);
              }
            };
          }
        }

      } catch (err) {
        console.error('Upload failed:', err);
        spinner.style.display = 'none';
        recordButton.classList.remove('disabled');
        responseText.textContent = '❌ Upload or response failed.';
      }
    };

    mediaRecorder.start();

    setTimeout(() => {
      mediaRecorder.stop();
      stream.getTracks().forEach(track => track.stop());
    }, 7000);
  } catch (err) {
    console.error('Mic error:', err);
    spinner.style.display = 'none';
    recordButton.classList.remove('disabled');
    responseText.textContent = '❌ Mic not available or permission denied.';
  }
});
