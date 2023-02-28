import sys
sys.path.insert(1, './src')

from flask_sock import Sock
from flask_socketio import SocketIO, emit
from PIL import Image
import numpy as np
import io
import flask
from flask import render_template
from detectAction import predict_image, words, accuracy
from flask import Flask

app = Flask(__name__)
socket = Sock(app)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pass-frame', methods=['POST'])
def handle_request():
    if 'file' not in flask.request.files:
        response = flask.jsonify({'message': 'No file part in the request'})
        response.status_code = 400
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    file = flask.request.files['file']
    imageBytes = io.BytesIO(file.read())
    imageData = Image.open(imageBytes)
    arrayOfImgData = np.asarray(imageData)
    print(arrayOfImgData)

    predict_image(arrayOfImgData)
    response = flask.jsonify({'message': 'File successfully uploaded'})
    response.status_code = 201
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get-predicted-word', methods=['GET'])
def pass_predicted_word():
    response = flask.jsonify({words, accuracy})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.status_code = 200
    return response

# @socket.route('/process-frame', methods=['GET'])
# def process_frame(sock):
#   while True :
#     frame = sock.receive()
#     if frame != "":
#       print("whats up")
#       numpydata = np.asarray(frame).astype("float16")
      # predict_image(numpydata)
    # sock.send("hi")
    
    # @socketio.route('/process-frame', methods=['GET'])


# @socketio.on('frame')
# def process_frame(frame):
#   print("whats up")
#   numpydata = np.asarray(frame).astype("float16")
  # predict_image(numpydata)
    

app.run(host="0.0.0.0", port=1234, debug=True)
