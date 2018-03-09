from threading import Thread
from textblob import TextBlob
import json
class ClientThread(Thread):
    def __init__(self, ip, port,conn,connected_users,threads,groups):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.connected_users = connected_users
        self.response = {}
        self.responseBytes = b''
        self.server_threads = threads
        self.groups = groups
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
            if data_dictionary['msgTo'] != 'unknown' and data_dictionary['rec'] == 'person':

                temp = TextBlob((data_dictionary['msg']))
                if temp.sentiment.polarity != 0 :
                    print("{} is {}".format(data_dictionary['username'],"happy" if temp.sentiment.polarity > 0 else "sad"))
                temp = temp.correct()
                data_dictionary['msg'] = temp.string
                msg = bytes(json.dumps(data_dictionary), 'utf-8')
                self.server_threads[self.connected_users[data_dictionary['msgTo']]
                ].conn.send(msg)
            elif data_dictionary['msgTo'] != 'unknown' and data_dictionary['rec'] == 'group':
                msg = bytes(json.dumps(data_dictionary), 'utf-8')
                data_dictionary['msg'] = TextBlob(data_dictionary['msg']).correct().string
                for clientThread in self.groups[data_dictionary['msgTo']]:
                    if clientThread != self:
                        clientThread.conn.send(msg)

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
                self.conn.send(self.responseBytes)
            else:
                self.prepare_msg("sorry {} is already taken".format(username),'server','info','failed',username)

                self.conn.send(self.responseBytes)
        elif command.startswith("**create_group"):
            group = command[len('**create_group'):].strip()
            if group not in self.groups:
                print("{} group has been created".format(group))
                self.groups[group] = []
                self.prepare_msg("group {} has been created".format(group), 'server', 'info', 'success', group)
                self.conn.send(self.responseBytes)
            else:
                self.prepare_msg("sorry group {} is already exists".format(group), 'server', 'info', 'failed', group)
                self.conn.send(self.responseBytes)
        elif command.startswith("**connect_to_group"):
            group = command[len('**connect_to_group'):].strip()
            if group in self.groups:
                print("{} has connected to group {}".format(data_dictionary['username'],group))
                self.groups[group].append(self.server_threads[self.connected_users[data_dictionary['username']]])
                self.prepare_msg("you are now connected to group {}".format(group), 'server', 'info', 'success', group)
                self.conn.send(self.responseBytes)
            else:
                self.prepare_msg("sorry group {} is not exists".format(group), 'server', 'info', 'failed', group)
                self.conn.send(self.responseBytes)
        else:
            self.prepare_msg("sorry this is unknown command", 'server', 'info', 'failed', ' ')
            self.conn.send(self.responseBytes)



    def prepare_msg(self,msg,username,type,status,data):
        self.response['msg'] = msg
        self.response['username'] = username
        self.response['type'] = type
        self.response['status'] = status
        self.response['data']  = data
        self.responseBytes = bytes(json.dumps(self.response),"utf-8")

