from gtts import gTTS
import os
import uuid

def generate_tts(text):
    tts = gTTS(text)
    filename = f"{uuid.uuid4().hex}.mp3"
    folder = "backend/static/audio"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    tts.save(path)
    return filename