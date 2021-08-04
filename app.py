from flask import Flask, jsonify, request, send_file, Response
from rembg.bg import remove
import numpy as np
import io
from PIL import Image
from base64 import b64decode

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
    data = request.json
    if 'image' not in data:
        return jsonify({
            "error": "No file received"
        })

    bytesImage = b64decode(data['image'])

    if bytesImage is not None:
        output_file_bytes = io.BytesIO()
        image = remove_background(bytesImage)
        image.save(output_file_bytes, format="PNG")
        return Response(
            output_file_bytes.getvalue(),
            mimetype="image/png"
        )


    return jsonify({
        "test": "nice"
    })