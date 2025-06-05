import openai
import os
import tempfile

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_file):
    try:
        # Save audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
            audio_file.save(temp_audio)
            temp_audio_path = temp_audio.name

        print("🔊 Transcribing audio:", temp_audio_path)

        with open(temp_audio_path, "rb") as f:
            transcript_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text"
            )
os.remove(temp_audio_path)

        transcript = transcript_response.strip()
        print("✅ Whisper transcript:", transcript)
        return transcript

    except Exception as e:
        print("❌ Whisper error:", e)
        return ""
