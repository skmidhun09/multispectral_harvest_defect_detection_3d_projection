import cv2
import jsonpickle
import numpy as np

import requests

# Making a get request
response = requests.get('http://127.0.0.1:5000/image/get')
resp = jsonpickle.decode(response.text)
nparr = np.frombuffer(resp, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
cv2.imshow('image', img)
cv2.waitKey(0)
