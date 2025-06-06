import openai
import os
import tempfile
import subprocess

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_file):
    try:
        # Save incoming audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
            audio_file.save(temp_audio)
            temp_input_path = temp_audio.name

        # Convert to .wav using ffmpeg
        temp_output_path = temp_input_path.replace(".webm", ".wav")
        subprocess.run([
            "ffmpeg", "-y", "-i", temp_input_path, temp_output_path
        ], check=True)

        # Transcribe
        with open(temp_output_path, "rb") as f:
            transcript_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text"
            )

        transcript = transcript_response.strip()
        print("✅ Whisper transcript:", transcript)

        # Clean up
        os.remove(temp_input_path)
        os.remove(temp_output_path)

        return transcript

    except Exception as e:
        print("❌ Whisper error:", e)
        return ""

