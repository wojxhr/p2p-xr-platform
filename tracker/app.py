import flask
from flask import Flask, request, jsonify, make_response
from flask_cors import *
import json


peerNum = 0
app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/register',methods=['GET','POST'])
def register():  # put application's code here
    data = flask.request.get_data()
    print(data)
    return 'Hello World!'

@app.route('/delete',methods=['GET','POST'])
def delete():
    pass

@app.route('/update',methods=['GET','POST'])
def heartbeat():
    pass

if __name__ == '__main__':
    app.run()
