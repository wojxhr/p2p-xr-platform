import flask
from flask import Flask, request, jsonify, make_response
from flask_cors import *
import json,time

nodeNum = 0
app = Flask(__name__)
CORS(app, supports_credentials=True)

mpd_list = dict()
ip_list = []

@app.route('/register',methods=['POST'])
def register():  # put application's code here
    data = flask.request.json
    print(data)
    ip = data['ip']
    ip_list.append(ip)
    print(ip_list)
    return 'register done!'