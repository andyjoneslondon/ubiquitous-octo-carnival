from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import json
import re

from gpt_logic import get_gpt_reply
from tts import generate_tts
from db import save_report, get_latest_status
from whisper_logic import transcribe_audio  # New import

app = Flask(__name__)
CORS(app, supports_credentials=True)

# -------------------- TEXT PROCESSING ROUTE --------------------
@app.route('/process_text', methods=['POST', 'OPTIONS'])
@cross_origin(origin='https://ubiquitous-octo-carnival.onrender.com',
              methods=['POST', 'OPTIONS'],
              headers=['Content-Type'],
              supports_credentials=True)
def process_text():
    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        print("✅ Received:", data)

        reply_json = get_gpt_reply(text)
        print("📥 GPT raw reply:", repr(reply_json))

        if not reply_json:
            print("❌ GPT returned empty response — check input and API key.")
            return jsonify({'error': 'GPT returned empty response'}), 500

        json_match = re.search(r"{.*}", reply_json, re.DOTALL)
        if not json_match:
            print("❌ Could not find JSON block in GPT reply")
            return jsonify({'error': 'Invalid GPT format'}), 500

        parsed = json.loads(json_match.group(0))
        intent = parsed['intent']
        location = parsed['location']

        if intent == "report":
            status = parsed.get('status', 'unknown')
            save_report(location, status)
            final_reply = f"Thanks. I've noted that {location} has {status}."
        elif intent == "query":
            status = get_latest_status(location)
            final_reply = f"{location} currently has {status}."
        else:
            final_reply = "Sorry, I couldn't understand your request."

        audio_filename = generate_tts(final_reply)
        audio_url = f"https://ubiquitous-octo-carnival-backend.onrender.com/audio/{audio_filename}" if audio_filename else None

        return jsonify({'reply': final_reply, 'audio_url': audio_url})

    except Exception as e:
        print("❌ ERROR in /process_text:", e)
        return jsonify({'error': 'Internal server error'}), 500

# -------------------- AUDIO PROCESSING ROUTE --------------------
@app.route('/process_audio', methods=['POST'])
@cross_origin(origin='https://ubiquitous-octo-carnival.onrender.com',
              methods=['POST'],
              supports_credentials=True)
def process_audio():
    try:
        audio_file = request.files.get('audio')
        if not audio_file:
            return jsonify({'error': 'No audio file uploaded'}), 400

        print("🎙️ Received audio file:", audio_file.filename)

        # 🔈 Transcribe with Whisper
        transcript = transcribe_audio(audio_file)
        if not transcript:
            return jsonify({'error': 'Whisper transcription failed'}), 500

        print("📝 Whisper transcript:", transcript)

        # 🧠 GPT analysis
        reply_json = get_gpt_reply(transcript)
        print("📥 GPT raw reply:", repr(reply_json))

        if not reply_json:
            return jsonify({'error': 'GPT returned empty response'}), 500

        json_match = re.search(r"{.*}", reply_json, re.DOTALL)
        if not json_match:
            return jsonify({'error': 'Invalid GPT format'}), 500

        parsed = json.loads(json_match.group(0))
        intent = parsed['intent']
        location = parsed['location']

        if intent == "report":
            status = parsed.get('status', 'unknown')
            save_report(location, status)
            final_reply = f"Thanks. I've noted that {location} has {status}."
        elif intent == "query":
            status = get_latest_status(location)
            final_reply = f"{location} currently has {status}."
        else:
            final_reply = "Sorry, I couldn't understand your request."

        audio_filename = generate_tts(final_reply)
        audio_url = f"https://ubiquitous-octo-carnival-backend.onrender.com/audio/{audio_filename}" if audio_filename else None

        return jsonify({
            'transcript': transcript,
            'reply': final_reply,
            'audio_url': audio_url
        })

    except Exception as e:
        print("❌ ERROR in /process_audio:", e)
        return jsonify({'error': 'Internal server error'}), 500

# -------------------- AUDIO FILE SERVING --------------------
@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory("static/audio", filename)

# -------------------- CORS TEST ROUTE --------------------
@app.route("/cors-test", methods=["OPTIONS"])
@cross_origin(origin='https://ubiquitous-octo-carnival.onrender.com',
              methods=['OPTIONS'],
              headers=['Content-Type'],
              supports_credentials=True)
def cors_test():
    return jsonify({"message": "CORS preflight successful"})

# -------------------- MAIN ENTRY --------------------
if __name__ == '__main__':
    app.run(debug=True)
