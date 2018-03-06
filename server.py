import socket
from socketserver import ThreadingMixIn
from ClientThread import ClientThread
class Server:
    def __init__(self,port=2004,buffer_size=20):
        self.TCP_IP = '0.0.0.0'
        self.TCP_PORT = port
        self.BUFFER_SIZE = buffer_size
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.TCP_IP, self.TCP_PORT))
        self.threads = {}
        self.connected_users = {}
        self.groups = {}
    def  start(self):
        connected_users = self.connected_users
        print("server started")
        while True:
            self.server.listen(4)
            (conn, (ip, port)) = self.server.accept()
            print(conn,ip,port)
            newthread = ClientThread(ip, port,conn=conn,connected_users=connected_users,threads=self.threads,groups=self.groups)
            newthread.start()
            self.threads[str(ip)+":"+str(port)] = newthread
            print(self.threads)


        for t in threads:
            t.join()
if __name__ == '__main__':
    server = Server()
    server.start()