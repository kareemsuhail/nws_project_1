def execute_command(room):
    if room.msg.startswith('**set_username'):
        username = room.msg[len('**set_username'):].strip()
        room.client.info['type'] = 'command'
        room.client.send(room.msg)
    if room.msg.startswith('**connect_with'):
        msgTo = room.msg[len('**connect_with'):].strip()
        room.client.info['msgTo'] = msgTo
        room.display_info("you are now connected to {}".format(msgTo))
def handle_server_commands(room,data):
    room.display_info("command was received from server ")
    if data['msg'] == '**set_username':
        room.client.info['username'] = data['data']
        room.display_info("username has been set successfully to {}".format(data['data']))

