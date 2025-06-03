from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt_logic import get_gpt_reply
from tts import generate_tts

app = Flask(__name__)
CORS(app)

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    reply = get_gpt_reply(text)
    audio_filename = generate_tts(reply)
    audio_url = f"/audio/{audio_filename}"

    return jsonify({'reply': reply, 'audio_url': audio_url})

@app.route('/audio/<filename>')
def serve_audio(filename):
    return app.send_static_file(f'audio/{filename}')

if __name__ == '__main__':
    app.run(debug=True)