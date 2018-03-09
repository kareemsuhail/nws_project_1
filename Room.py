import unicurses
from client import Client
import threading
import time
import json
import sys
from commandsManager import execute_command ,handle_server_commands
class Room:
    def __init__(self):
        self.stdscr = unicurses.initscr()
        self.client = Client()
        self.client.connect()
        self.receive_data_thread = threading.Thread(target=self.display_received_data)
        self.receive_data_thread.daemon = True
        unicurses.start_color()
        unicurses.init_pair(1,unicurses.COLOR_GREEN,unicurses.COLOR_BLACK)
        self.height, self.width = self.stdscr.getmaxyx()
        self.displayWindow = unicurses.newwin(self.height-6,self.width,0,0)
        self.infoWindow = unicurses.newwin(3,self.width,self.height-6,0)
        self.inputWindow = unicurses.newwin(3,self.width,self.height-3,0)
        self.inputWindow.move(1,1)
        self.msg = ''
        self.init_display_screen()
        self.init_info_screen()
        try:
            self.receive_data_thread.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

    def run(self):

        self.inputWindow.box()

        while(True):
            key = self.inputWindow.getch()
            if key != 10 and key!=27:
                self.msg = self.msg + chr(key)
            elif key ==10:
                if(self.msg.startswith('**')):
                    execute_command(self)
                    self.clear_input(display_msg=False)
                else:
                    self.client.info['type'] = 'msg'
                    self.client.send(self.msg)
                    self.clear_input()
            elif key == 0x08:
                self.msg = self.msg[:len(msg)-2]
                self.inputWindow.clear()
                self.inputWindow.move(1, 1)
                self.inputWindow.addstr(msg)
            elif key ==27 :
                try:
                    self.client.client.close()
                    self.receive_data_thread._stop()
                except:
                    pass
                sys.exit()
    def clear_input(self,display_msg=True):
        if(display_msg):
            self.display_text(self.msg)
        self.msg = ''
        self.inputWindow.clear()
        self.inputWindow.box()
        self.inputWindow.move(1,1)
    def init_info_screen(self):
        self.infoWindow.box()
        self.infoWindow.move(0, int(self.width / 2) - 3)
        self.infoWindow.addstr(" Info ")
        self.infoWindow.refresh()
    def init_display_screen(self):
        self.displayWindow.box()
        self.displayWindow.move(0,int(self.width/2)-5)
        self.displayWindow.addstr(" chat app ")
        self.displayWindow.refresh()
    def display_text(self,text,username='you'):
        y,x = self.displayWindow.getyx()
        if(y==self.height-5):
            self.clear_display_text()
            y, x = self.displayWindow.getyx()
        self.displayWindow.move(y+1,1)
        self.displayWindow.addstr("{}:".format(username),unicurses.color_pair(1))
        self.displayWindow.addstr(text)
        self.displayWindow.refresh()
    def display_info(self,text,type="info"):
        self.clear_info_window()
        y, x = self.infoWindow.getyx()
        if (y == self.height - 5):
            self.init_info_screen()
            y, x = self.infoWindow.getyx()
        self.infoWindow.move(y + 1, 1)
        self.infoWindow.addstr("{}:".format(type), unicurses.color_pair(1))
        self.infoWindow.addstr(text)
        self.infoWindow.refresh()

    def clear_display_text(self):
        self.displayWindow.clear()
        self.init_display_screen()
    def clear_info_window(self):
        self.infoWindow.clear()
        self.init_info_screen()
    def display_received_data(self):
        while(True):
            try:
                data = self.client.receive()
                data_dict = json.loads(data.replace("'", '"'))
                if data_dict['type'] == 'msg':
                    self.display_text(text=data_dict['msg'], username=data_dict['username'])
                elif data_dict['type'] == 'info':

                    self.display_info(data_dict['msg'])
                elif data_dict['type'] == 'command':
                    handle_server_commands(self, data_dict)
            except Exception as ex:
                self.receive_data_thread._stop()
                raise ex
                continue
if __name__ == '__main__':
    room = Room()
    room.run()
