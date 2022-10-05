import flask
from flask import Flask, request, jsonify, make_response
from flask_cors import *
import json,time

nodeNum = 0
app = Flask(__name__)
CORS(app, supports_credentials=True)

mpd_list = dict()


@app.route('/regiter',methods=['POST'])
def register():  # put application's code here


    return 'register done!'