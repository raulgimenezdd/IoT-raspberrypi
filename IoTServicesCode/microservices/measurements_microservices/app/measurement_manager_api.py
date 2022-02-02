from flask import Flask, request
from flask_cors import CORS
import os
from measurement_manager import *

app = Flask(__name__)
CORS(app)

@app.route('/measurements/register/', methods=['POST'])
def set_measurement():
    params = request.get_json()
    measurements_register(params)
    return {"result":"record inserted"}, 201

@app.route('/measurements/retrieve/')
def get_measurements():
    return measurements_retriever()


#HOST = os.getenv('HOST')
#PORT = os.getenv('PORT')
app.run(host="0.0.0.0", port="5001")