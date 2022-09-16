import flask
from flask import Flask, request, jsonify, make_response
from flask_cors import *
import json,time

peerNum = 0
app = Flask(__name__)
CORS(app, supports_credentials=True)
node=dict()
connectPair={}


@app.route('/register',methods=['GET','POST'])
def register():  # put application's code here
    global peerNum
    data = flask.request.json
    peerId = data['peerId']
    ip = data['ipAddress']
    curTime = time.time()
    node[peerId] = {"ipAddress":ip,"curTime":curTime}
    peerNum+=1
    print(node)
    return 'register done!'

@app.route('/delete',methods=['GET','POST'])
def delete():
    data = flask.request.json
    ip = data['ipAddress']
    for key in list(node.keys()):
        if node[key]['ipAddress'] == ip:
            del node[key]
    print(node)
    return "delete done."

@app.route('/applyid',methods=['POST'])
def apply():
    # TODO:直接改成返回其连接的节点ID，以及其身份，目前是先以时间来衡量，显然不对
    data = flask.request.json
    id = data['id']
    targetId = None
    role = None
    # 临时测试用
    if id not in node:
        return targetId
    else:
        time = node[id]['curTime']

    for k,v in connectPair.items():
        if v == id:
            targetId=k
            role='precessor'
            break

    if targetId is None:
        for k,v in node.items():
            # 目前的逻辑是，连接时间靠前的必然具有缓存
            if v['curTime'] < time:
                targetId = k
                role='youth'
                connectPair[id]=targetId

    if targetId:
        content = json.dumps({"targetId":targetId,"role":role})
    else:
        content = ""
    return content


@app.route('/update',methods=['POST'])
def heartbeat():
    pass

if __name__ == '__main__':
    app.run(debug=True)
