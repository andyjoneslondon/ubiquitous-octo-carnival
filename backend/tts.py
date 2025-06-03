from gtts import gTTS
import os
import uuid

def generate_tts(text):
    try:
        print("Generating TTS for:", text)
        tts = gTTS(text)
        filename = f"{uuid.uuid4().hex}.mp3"
        folder = "static/audio"
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        print("Saving TTS to:", path)
        tts.save(path)
        return filename
    except Exception as e:
        print("❌ TTS generation failed:", e)
        return None
