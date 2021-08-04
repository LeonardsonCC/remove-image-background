from flask import Flask, jsonify, request
from rembg.bg import remove
import numpy as np
import io
from PIL import Image

input_path = 'input.png'
output_path = 'out.png'
ALLOWED_EXTENSIONS = {'png'}

app = Flask(__name__)

print("Starting")
def remove_background(stringFile):
    f = np.fromstring(stringFile, dtype=np.uint8)
    result = remove(f)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    img.save(output_path)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def route_index():
    return jsonify({
        "test": "ok"
    })

@app.route("/remove-background", methods=["POST"])
def route_remove_background():
    if 'file' not in request.files:
        return jsonify({
            "error": "No file received"
        })
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            "error": "File not found"
        })

    if file and allowed_file(file.filename):
        file_bytes = io.BytesIO()
        file.save(file_bytes)
        remove_background(file.getvalue())
        return jsonify({
            "data": "nice"
        })

    return jsonify({
        "test": "nice"
    })