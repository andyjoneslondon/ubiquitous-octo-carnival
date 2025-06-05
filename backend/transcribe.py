import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(file_path):
    try:
        print("🔊 Sending audio to Whisper:", file_path)
        with open(file_path, "rb") as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file)
            text = response["text"]
            print("📝 Transcription:", text)
            return text
    except Exception as e:
        print("❌ Whisper transcription failed:", e)
        return None
