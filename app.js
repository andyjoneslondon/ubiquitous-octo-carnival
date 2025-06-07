const recordButton = document.getElementById('recordButton');
const responseText = document.getElementById('response');
const transcriptText = document.getElementById('transcript');
const spinner = document.getElementById('spinner');
const audioPlayer = document.getElementById('audio');

let mediaRecorder;
let chunks = [];

recordButton.addEventListener('click', async () => {
  // 🔓 Unlock autoplay policies with silent audio
  const unlockAudio = new Audio('data:audio/mp3;base64,//uQxAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAACcQCA...');
  unlockAudio.play().catch(() => {});

  // 🚫 Reset audio element to prevent replay
  audioPlayer.pause();
  audioPlayer.src = '';
  audioPlayer.load();

  // UI reset
  responseText.textContent = '';
  transcriptText.textContent = '';
  audioPlayer.style.display = 'none';

  recordButton.classList.add('disabled');
  spinner.style.display = 'block';

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // 🕒 Wait 500ms to allow mic to warm up
    await new Promise(resolve => setTimeout(resolve, 500));

    // 🔊 Beep to indicate start of recording
    const startBeep = new Audio('beep.wav');
    await startBeep.play();

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
            console.warn('Autoplay blocked. User must tap play manually.', err);
            responseText.textContent += '\n🔈 Tap the player above to hear the reply.';
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

    // ⏱️ Stop after 6 seconds and play end beep
    setTimeout(async () => {
      const stopBeep = new Audio('beep.wav');
      await stopBeep.play();

      mediaRecorder.stop();
      stream.getTracks().forEach(track => track.stop());
    }, 6000);

  } catch (err) {
    console.error('Mic error:', err);
    spinner.style.display = 'none';
    recordButton.classList.remove('disabled');
    responseText.textContent = '❌ Mic not available or permission denied.';
  }
});

// ✅ Register the service worker here, outside the event handler
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js')
    .then(() => console.log('✅ Service worker registered'))
    .catch(err => console.error('Service worker error:', err));
}
