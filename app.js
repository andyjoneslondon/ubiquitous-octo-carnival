const recordButton = document.getElementById('recordButton');
const responseText = document.getElementById('response');
const transcriptText = document.getElementById('transcript');
const spinner = document.getElementById('spinner');
const audioPlayer = document.getElementById('audio');

let mediaRecorder;
let chunks = [];

recordButton.addEventListener('click', async () => {
  // Prime Safari's audio policy
  const unlockAudio = new Audio('data:audio/mp3;base64,//uQxAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAACcQCA...');
  unlockAudio.play().catch(() => {});

  responseText.textContent = '';
  transcriptText.textContent = '';
  audioPlayer.style.display = 'none';

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
            console.warn('Autoplay blocked:', err);
            responseText.textContent += '\n🔈 Tap play above to hear the reply.';
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
