import socket
import sys
import json
class Client:
    def __init__(self, port=2004, buffer_size=2000):
        self.host = socket.gethostname()
        self.port = port
        self.BUFFER_SIZE = buffer_size
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.info = {}
        self.info['port'] = port
        self.info['ip'] = socket.gethostbyname(socket.gethostname())
        self.info['s_ip'] = socket.gethostbyname(socket.gethostname())
        self.info['rec'] = 'person'
        self.info['username'] = sys.argv[0] if len(sys.argv) > 1 else "unknown"
        self.info['msgTo'] = sys.argv[1] if len(sys.argv) > 2 else "unknown"
        self.info['msg'] = 'no msg provided'
        self.info['type'] = 'msg'

    def connect(self):
        self.client.connect((self.host, self.port))

    def send(self, msg):
        self.info['msg'] = msg
        self.client.send(bytes(json.dumps(self.info), 'utf-8'))

    def receive(self):
        while True:
            data = self.client.recv(self.BUFFER_SIZE).decode('utf8')
            if data:
                return data


if __name__ == '__main__':
    client = Client()
    client.connect()
    client.send("welcome")
    client.receive()
