from threading import Thread
import json
class ClientThread(Thread):
    def __init__(self, ip, port,conn,connected_users,threads):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.connected_users = connected_users
        self.response = {}
        self.responseBytes = b''
        self.server_threads = threads
        print("[+] new client has connected " + ip + ":" + str(port))

    def run(self):
        while True:
            data = self.conn.recv(2048)
            data_dictionary =  json.loads(data.decode('utf8').replace("'", '"'))


            if (data_dictionary['type'] == 'command'):
                self.execute_command(data_dictionary)
                continue
            print(data_dictionary)
            if data_dictionary['username'] == 'unknown':
                self.prepare_msg("sorry you have to specify your username", 'server', 'info', 'failed',
                                 data_dictionary['username'])
                self.conn.send(self.responseBytes)
                continue
            if data_dictionary['msgTo'] != 'unknown':
                msg = bytes(json.dumps(data_dictionary),'utf-8')
                print(self.server_threads)

                self.server_threads[self.connected_users[data_dictionary['msgTo']]
                ].conn.send(msg)
            else:
                self.prepare_msg("sorry you have to specify msg receiver", 'server', 'info', 'failed', data_dictionary['username'])
                self.conn.send(self.responseBytes)
    def execute_command(self,data_dictionary):
        command = data_dictionary['msg']
        if command.startswith("**set_username"):
            username = command[len('**set_username'):].strip()
            if username not in self.connected_users :
                print("{} has been connected".format(username))
                user_data = str(data_dictionary['s_ip']+":"+str(self.port))
                self.connected_users[username] = user_data
                self.prepare_msg("**set_username",'server','command','success',username)
                print(self.responseBytes)
                self.conn.send(self.responseBytes)
            else:
                self.prepare_msg("sorry {} is already taken".format(username),'server','info','failed',username)
                print(self.responseBytes)
                self.conn.send(self.responseBytes)


    def prepare_msg(self,msg,username,type,status,data):
        self.response['msg'] = msg
        self.response['username'] = username
        self.response['type'] = type
        self.response['status'] = status
        self.response['data']  = data
        self.responseBytes = bytes(json.dumps(self.response),"utf-8")

