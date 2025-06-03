from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt_logic import get_gpt_reply
from tts import generate_tts

app = Flask(__name__)
CORS(app)

@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        print("Received:", data)

        text = data.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        reply = get_gpt_reply(text)
        print("GPT reply:", reply)

        audio_filename = generate_tts(reply)
        print("Audio filename:", audio_filename)

        audio_url = f"/audio/{audio_filename}"
        return jsonify({'reply': reply, 'audio_url': audio_url})
    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    return app.send_static_file(f'audio/{filename}')

if __name__ == '__main__':
    app.run(debug=True)
