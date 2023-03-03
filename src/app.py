import io
import asyncio
import time
import flask
import random
import requests
import numpy as np
from PIL import Image
from flask import Flask
from flask_sock import Sock
from detectAction import predict_image
from flask import render_template
from flask_socketio import SocketIO, emit
from requests_toolbelt.multipart import decoder
# from fetch_data import FetchData
import sys
sys.path.insert(1, './src')

app = Flask(__name__)
socket = Sock(app)
# socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/get-predicted-word', methods=['GET'])
# def pass_predicted_word():
#     response = flask.jsonify({'words': words, 'accuracy': accuracy})
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.status_code = 200
#     return response


# @app.route('/rand-num', methods=['GET'])
# def generate_random_number():
#     response = flask.make_response(str(random.randint(0, 999)))
#     response.mimetype = "text/plain"
#     response.status_code = 200
#     return response


def FetchData(send_data_func):
    session = requests.Session()
    url = "https://10.132.125.83:8080/stream.mjpeg"

    response = session.get(url, stream=True, verify=False)
    print(response.status_code)
    if response.status_code != 200:
        time.sleep(2)
        print("Trying again")
        FetchData()
        return
    boundary = response.headers['Content-Type'].split('boundary=')[1]
    delimeter = ("\r\n--" + boundary).encode()

    fileIndex = 0
    for line in response.iter_lines(delimiter=delimeter, decode_unicode=True):
        if line:
            image_bytes = line.split(b'\r\n\r\n')[1]
            imageBytes = io.BytesIO(image_bytes)
            imageData = Image.open(imageBytes)
            arrayOfImgData = np.asarray(imageData)
            print("got total " + str(len(image_bytes)) + " bytes")
            f = open("temp/file" + str(fileIndex) + ".jpeg", "wb")
            f.write(image_bytes)
            fileIndex += 1
            words, accuracy = predict_image(arrayOfImgData)
            # print(words, accuracy)
            send_data_func(words, accuracy)
    print("Fetching stopped")


def send_detected_word_closure(sock):
    def send_detected_word(words, accuracy):
        # if words and accuracy > 0:
        print("sending")
        sock.send("{'words': " + words + ", 'accuracy': " + str(accuracy) + "}")
        return
    return send_detected_word


@socket.route('/get-result', methods=['GET'])
def process_frame(sock):
    print("before calling FetchData")
    FetchData(send_detected_word_closure(sock))
    print("after calling FetchData")


# @socketio.on('frame')
# def process_frame(frame):
#   print("whats up")
#   numpydata = np.asarray(frame).astype("float16")
    # predict_image(numpydata)

app.run(host="0.0.0.0", port=1234, debug=True)
