from flask import Flask, request, jsonify, send_file
import os
import uuid
import subprocess
import tempfile

app = Flask(__name__)

@app.route("/")
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/api/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return jsonify({
            "status":"error",
            "message":"No file"
        })

    file = request.files["file"]

    uid = str(uuid.uuid4())

    temp_dir = tempfile.gettempdir()

    input_path = os.path.join(
        temp_dir,
        uid + "_" + file.filename
    )

    output_path = os.path.join(
        temp_dir,
        uid + ".mp3"
    )

    file.save(input_path)

    try:

        subprocess.run([
            "ffmpeg",
            "-i",
            input_path,
            "-vn",
            "-ar",
            "44100",
            "-ac",
            "2",
            "-b:a",
            "192k",
            output_path
        ], check=True)

        return send_file(
            output_path,
            as_attachment=True,
            download_name="converted.mp3"
        )

    except Exception as e:

        return jsonify({
            "status":"error",
            "message":str(e)
        })

app = app