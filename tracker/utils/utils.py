
import socket

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def get_index(filelist):
    post = {}
    for file in filelist:
        left = file.find('k')
        right = file.find('.m4')
        index = file[left + 2:right]
        if index not in post:
            post[index] = [file]
        else:
            post[index].append(file)
    return post

if __name__ == '__main__':
    print(get_host_ip())