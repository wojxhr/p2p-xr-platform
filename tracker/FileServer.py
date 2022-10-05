import os,json
import requests,threading
from http.server import HTTPServer, BaseHTTPRequestHandler,SimpleHTTPRequestHandler
from utils import net


data = {"result":"Logxx"}
StorageHost = ('0.0.0.0', 8080)
FileServerHost = ('0.0.0.0', 8000)
TrackerURL = None

#TODO:file manager
class FileManager:
    """
    对下载的chunk文件进行管理，需要具备以下功能：
    1.文件上报，对下载的文件定期统计上报给tracker
    2.cache替换，控制文件目录的大小，定期替换访问次数低的文件
    3.日志管理，记录每一个文件的访问次数，方便进行清理
    4.文件清理，file server关闭时清理所有文件
    """
    def __init__(self):
        self.video_path = './video'
        self.audio_path = './audio'
        self.ip = None

    def register(self):
        if not self.ip:
            self.ip = net.get_host_ip()

    def report(self):
        videoFiles = os.listdir('./video')
        audioFiles = os.listdir('./audio')


    def replace(self):
        pass
    def record(self):
        pass
    def clear(self):
        pass

    def run(self):
        pass
class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)


class Resquest(BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        """ Sets headers required for CORS """
        self.send_header('Content-type', 'application/octet-stream')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type,MediaType,representationId,index")

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


    def do_POST(self):
        self.send_response(200, "ok")
        self._send_cors_headers()
        self.end_headers()
        # post分成两部分，一部分是来自本机的chunk上传请求，一部分来自于其他peer的request请求
        datas = self.rfile.read(int(self.headers['content-length']))

        contentType = self.headers['Content-Type']
        if 'mp4' in contentType:
            # mediatype需要从header中分割一下
            index = self.headers['index']
            mediatype = contentType[0:5]
            representationId = self.headers['representationId']
            # save in local file
            if mediatype == 'video':
                with open('./video/' + representationId + '_' + index+'.m4v','wb') as f:
                    f.write(datas)
            elif mediatype == 'audio':
                with open('./audio/' + representationId + '_' + index+'.m4a','wb') as f:
                    f.write(datas)
            else:
                pass
        else:
            request = json.loads(datas)
            print(request)


        # print("do post:", self.path, self.client_address, datas)
        self.wfile.write(json.dumps(data).encode())

def File_Server():
    httpd = HTTPServer(FileServerHost, CORSRequestHandler)
    print("Starting file server, listen at: %s:%s\n" % FileServerHost)
    httpd.serve_forever()

def Storage():
    server = HTTPServer(StorageHost, Resquest)
    print("Starting storage server, listen at: %s:%s\n" % StorageHost)
    server.serve_forever()

def FileMonitor():
    monitor = FileManager()


if __name__ == '__main__':
    # t1 = threading.Thread(target=File_Server)
    # t2 = threading.Thread(target=Storage)

    # t1.start()
    # t2.start()
    FileMonitor()
