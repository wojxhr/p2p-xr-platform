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

def append_MPD_List(ip,Object,type):
    if type == 'video':
        for index in Object:
            if index not in mpd_list['videoList']:
                mpd_list['videoList'][index] = []
                for file in Object[index]:
                    url = 'http://' + ip + ':8000' + '/video/' + file
                    mpd_list['videoList'][index].append(url)
            else:
                for file in Object[index]:
                    url = 'http://' + ip + ':8000' + '/video/' + file
                    mpd_list['videoList'][index].append(url)
    else:
        for index in Object:
            if index not in mpd_list['audioList']:
                mpd_list['audioList'][index] = []
                for file in Object[index]:
                    url = 'http://' + ip + ':8000' + '/audio/' + file
                    mpd_list['audioList'][index].append(url)
            else:
                for file in Object[index]:
                    url = 'http://' + ip + ':8000' + '/audio/' + file
                    mpd_list['audioList'][index].append(url)

@app.route('/register',methods=['POST'])
def register():  # put application's code here
    raw = request.get_data()
    data = json.loads(raw)
    ip = data['ip']
    ip_list.append(ip)
    print(ip_list)
    return 'register done!'

@app.route('/report',methods=['POST'])
def report():
    raw = request.get_data()
    data = json.loads(raw)
    ip = data['ip']
    videoObject = data['videoObject']
    audioObject = data['audioObject']
    # 存进mpd_list，以url的形式存在
    append_MPD_List(ip,videoObject,'video')
    append_MPD_List(ip,audioObject,'audio')

    print(mpd_list)
    return 'Update.'

@app.route('/request',methods=['POST'])
def chunkRequest():
    pass

if __name__ == '__main__':
    app.run(debug=True)