from flask import Flask, jsonify, request, send_file, Response
from rembg.bg import remove
import numpy as np
import io
from PIL import Image

input_path = 'input.png'
output_path = 'out.png'
ALLOWED_EXTENSIONS = {'png'}

app = Flask(__name__)

def remove_background(stringFile):
    f = np.fromstring(stringFile, dtype=np.uint8)
    result = remove(f)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    return img

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

        output_file_bytes = io.BytesIO()
        image = remove_background(file.getvalue())
        image.save(output_file_bytes, format="PNG")
        return Response(
            output_file_bytes.getvalue(),
            mimetype="image/png"
        )


    return jsonify({
        "test": "nice"
    })