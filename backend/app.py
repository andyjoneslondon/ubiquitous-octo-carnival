from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import re

from gpt_logic import get_gpt_reply
from tts import generate_tts
from db import save_report, get_latest_status

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://ubiquitous-octo-carnival.onrender.com"}}, supports_credentials=True)

@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        print("Received:", data)

        reply_json = get_gpt_reply(text)
        print("GPT raw reply:", repr(reply_json))

        # Extract just the JSON block from GPT reply
        json_match = re.search(r"{.*}", reply_json, re.DOTALL)
        if not json_match:
            print("❌ Could not find JSON block in GPT reply")
            return jsonify({'error': 'Invalid GPT format'}), 500

        try:
            parsed = json.loads(json_match.group(0))
            intent = parsed['intent']
            location = parsed['location']
        except Exception as e:
            print("❌ JSON decode failed:", e)
            return jsonify({'error': 'Invalid GPT JSON format'}), 500

        if intent == "report":
            status = parsed.get('status', 'unknown')
            save_report(location, status)
            final_reply = f"Thanks. I've noted that {location} has {status}."
        elif intent == "query":
            status = get_latest_status(location)
            final_reply = f"{location} currently has {status}."
        else:
            final_reply = "Sorry, I couldn't understand your request."

        # Generate spoken response
        audio_filename = generate_tts(final_reply)
        if not audio_filename:
            print("❌ TTS failed.")
            return jsonify({'reply': final_reply, 'audio_url': None})

        print("Audio filename:", audio_filename)
        audio_url = f"https://ubiquitous-octo-carnival-backend.onrender.com/audio/{audio_filename}"

        return jsonify({'reply': final_reply, 'audio_url': audio_url})
    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory("static/audio", filename)

if __name__ == '__main__':
    app.run(debug=True)
