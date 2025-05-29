from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
from werkzeug.utils import secure_filename

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_text = request.form.get("text")
    if not user_text:
        return jsonify({"error": "No text provided."}), 400
    try:
        resp = requests.post(f"{BACKEND_URL}/llm/answer", json={
            "query": user_text,
            "context": [],
            "query_type": "market_brief"
        }, timeout=60)
        resp.raise_for_status()
        answer = resp.json().get("answer", "No answer.")
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/voice", methods=["POST"])
def voice():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded."}), 400
    audio = request.files['audio']
    filename = secure_filename(audio.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio.save(filepath)
    try:
        with open(filepath, "rb") as f:
            files = {"audio": (filename, f, audio.mimetype)}
            resp = requests.post(f"{BACKEND_URL}/agent", files=files, timeout=120)
            resp.raise_for_status()
            data = resp.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/audio/<filename>")
def audio_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
