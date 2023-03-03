import io
import requests
from requests_toolbelt.multipart import decoder
from detectAction import predict_image


def FetchData():
  session = requests.Session()
  # fileIndex = 0
  url = "https://10.132.125.83:8080/stream.mjpeg"

  with session.get(url, stream=True, verify=False) as resp:
    boundary = resp.headers['Content-Type'].split('boundary=')[1]
    delimeter = ("\r\n--" + boundary).encode()

    for line in resp.iter_lines(delimiter=delimeter, decode_unicode=True):
      if line:
          image_bytes = line.split(b'\r\n\r\n')[1]
          predict_image(image_bytes)
          # f = open("out.txt", "ab")
          # f.write(line)
          # f = open("temp/file" + str(fileIndex) + ".jpeg", "wb")
          # f.write(image_bytes)
          # f = open("temp/file" + str(fileIndex) + ".txt", "wb")
          # f.write(image_bytes)
          # fileIndex += 1
          # break


FetchData()
