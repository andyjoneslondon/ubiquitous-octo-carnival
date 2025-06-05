const recordButton = document.getElementById('recordButton');
const responseText = document.getElementById('response');
const transcriptText = document.getElementById('transcript');
const spinner = document.getElementById('spinner');
const audioPlayer = document.getElementById('audio');

let mediaRecorder;
let chunks = [];

recordButton.addEventListener('click', async () => {
  responseText.textContent = '';
  transcriptText.textContent = '';
  audioPlayer.style.display = 'none';

  recordButton.disabled = true;
  spinner.style.display = 'block';

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    chunks = [];

    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunks, { type: 'audio/webm' }); // ✅ Use supported format
      console.log('Blob type:', blob.type);
      const formData = new FormData();
      formData.append('audio', blob, 'input.webm'); // ✅ Match filename to MIME

      try {
        const response = await fetch('https://ubiquitous-octo-carnival-backend.onrender.com/process_audio', {
          method: 'POST',
          body: formData
        });

        const result = await response.json();

        spinner.style.display = 'none';
        recordButton.disabled = false;

        if (result.transcript) {
          transcriptText.textContent = `📝 You said: "${result.transcript}"`;
        }

        if (result.reply) {
          responseText.textContent = `🤖 ${result.reply}`;
        }

        if (result.audio_url) {
          audioPlayer.src = result.audio_url;
          audioPlayer.style.display = 'block';
          audioPlayer.play();
        }
      } catch (err) {
        console.error('Upload failed:', err);
        spinner.style.display = 'none';
        recordButton.disabled = false;
        responseText.textContent = '❌ Upload or response failed.';
      }
    };

    mediaRecorder.start();

    setTimeout(() => {
      mediaRecorder.stop();
      stream.getTracks().forEach(track => track.stop());
    }, 7000); // Stop recording after 7 seconds

  } catch (err) {
    console.error('Mic error:', err);
    spinner.style.display = 'none';
    recordButton.disabled = false;
    responseText.textContent = '❌ Mic not available or permission denied.';
  }
});
