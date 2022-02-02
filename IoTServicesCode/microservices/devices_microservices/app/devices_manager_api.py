import os
from flask import Flask, request
from flask_cors import CORS

from devices_manager import *

app = Flask(__name__)
CORS(app)

@app.route('/devices/register/', methods=['POST'])
def save_deviceinfo():
    params = request.get_json()
    devices_register(params)
    return {"result": "record inserted"}, 201

@app.route('/devices/retrieve/')
def retrieve_devices():
    return devices_retriever()

app.run(host="0.0.0.0", port="5002")