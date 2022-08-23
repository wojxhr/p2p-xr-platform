import flask
from flask import Flask, request, jsonify, make_response
from flask_cors import *
import json


peerNum = 0
app = Flask(__name__)
CORS(app, supports_credentials=True)
node=dict()
node_test = []


@app.route('/register',methods=['GET','POST'])
def register():  # put application's code here
    global peerNum
    data = flask.request.json
    peerId = data['peerId']
    node[peerId] = {"videoinfo":1,"segmentinfo":2}
    peerNum+=1
    print(node)
    return 'register done!'

@app.route('/delete',methods=['GET','POST'])
def delete():
    data = flask.request.json
    peerId = data['peerId']
    del node[peerId]
    print(node)
    return "delete done."

@app.route('/applyid',methods=['GET'])
def apply():
    content = json.dumps(node)
    print(content)
    return content


@app.route('/update',methods=['POST'])
def heartbeat():
    pass

if __name__ == '__main__':
    app.run(debug=True)
