import flask
from flask import Flask, request, jsonify, make_response
from flask_cors import *
import json,time

nodeNum = 0
app = Flask(__name__)
CORS(app, supports_credentials=True)

#TODO:后续加入一层tile
mpd_list = {"videoList":{},"audioList": {}}
#TODO:后续更改为记录ip地址及其节点情况的map
ip_list = []

changed = False

def append_MPD_List(ip,Object,type):
    global changed
    if type == 'video':
        for index in Object:
            if index not in mpd_list['videoList']:
                mpd_list['videoList'][index] = []
                for file in Object[index]:
                    url = 'http://' + ip + ':8000' + '/video/' + file
                    mpd_list['videoList'][index].append(url)
                changed = True
            else:
                for file in Object[index]:
                    url = 'http://' + ip + ':8000' + '/video/' + file
                    if url not in mpd_list['videoList'][index]:
                        mpd_list['videoList'][index].append(url)
                        changed = True
    else:
        for index in Object:
            if index not in mpd_list['audioList']:
                mpd_list['audioList'][index] = []
                for file in Object[index]:
                    url = 'http://' + ip + ':8000' + '/audio/' + file
                    mpd_list['audioList'][index].append(url)
                changed = True
            else:
                for file in Object[index]:
                    url = 'http://' + ip + ':8000' + '/audio/' + file
                    if url not in mpd_list['audioList'][index]:
                        mpd_list['audioList'][index].append(url)
                        changed = True

def check_MPD_List(ip,Object,type):
    if type == 'video':
        for index in list(mpd_list['videoList'].keys()):
            # 这个index的所有文件都消失了
            if index not in Object:
                del mpd_list['videoList'][index]
                changed = True
            else:
                # 这里使用临时list，避免遍历时删除元素的错误
                for url in list(mpd_list['videoList'][index]):
                    pos = url.find('video/')
                    filename = url[pos+6:]
                    if filename not in Object[index]:
                        mpd_list['videoList'][index].remove(url)
                        changed = True
    else:
        for index in list(mpd_list['audioList'].keys()):
            if index not in Object:
                del mpd_list['audioList'][index]
                changed = True
            else:
                for url in list(mpd_list['audioList'][index]):
                    pos = url.find('audio/')
                    filename = url[pos+6:]
                    if filename not in Object[index]:
                        mpd_list['audioList'][index].remove(url)
                        changed = True

def get_Chunk_Url(data):
    mediaType = data['mediaType']
    index = str(data['index'])
    if mediaType=='video':
        if index in mpd_list['videoList']:
            filename = data['representationId'] + '_' + index + '.m4v'
            for url in mpd_list['videoList'][index]:
                if filename in url:
                    return url
    else:
        if index in mpd_list['audioList']:
            filename = data['representationId'] + '_' + index + '.m4a'
            for url in mpd_list['audioList'][index]:
                if filename in url:
                    return url
    return None

@app.route('/register',methods=['POST'])
def register():  # put application's code here
    global nodeNum
    raw = request.get_data()
    data = json.loads(raw)
    ip = data['ip']
    ip_list.append(ip)
    nodeNum+=1
    return 'register done!'

@app.route('/report',methods=['POST'])
def report():
    global changed
    raw = request.get_data()
    data = json.loads(raw)
    ip = data['ip']
    videoObject = data['videoObject']
    audioObject = data['audioObject']
    # 存进mpd_list，以url的形式存在
    # TODO:每次上传时除了添加新的还要检查旧的还在不在
    append_MPD_List(ip,videoObject,'video')
    append_MPD_List(ip,audioObject,'audio')
    check_MPD_List(ip,videoObject,'video')
    check_MPD_List(ip,audioObject,'audio')
    if changed:
        print(mpd_list)
        changed = False
    return 'Update.'

@app.route('/request',methods=['POST','GET'])
def chunkRequest():
    if request.method == 'GET':
        return 'hello world'
    else:
        raw = request.get_data()
        data = json.loads(raw)
        url = get_Chunk_Url(data)
        
        if url:
            return url
        else:
            return "NO URL"
        

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

    # from gevent import pywsgi
    # server = pywsgi.WSGIServer(('0.0.0.0',5000),app)

    # from wsgiref.simple_server import make_server
    # server = make_server('0.0.0.0',5000,app)
    # server.serve_forever()
    # app.run()
    