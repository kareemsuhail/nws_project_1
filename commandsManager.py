def execute_command(room):
    if room.msg.startswith('**set_username'):
        room.client.info['type'] = 'command'
        room.client.send(room.msg)
    if room.msg.startswith('**connect_with'):
        room.client.info['rec'] = 'person'
        msgTo = room.msg[len('**connect_with'):].strip()
        room.client.info['msgTo'] = msgTo
        room.display_info("you are now connected to {}".format(msgTo))
    if room.msg.startswith('**create_group'):
        room.client.info['type'] = 'command'
        room.client.send(room.msg)
    if room.msg.startswith("**connect_to_group"):
        group = room.msg[len("**connect_to_group"):].strip()
        room.client.info['msgTo'] = group
        room.client.info['type'] = 'command'
        room.client.info['rec'] = 'group'
        room.client.send(room.msg)


def handle_server_commands(room, data):
    room.display_info("command was received from server ")
    if data['msg'] == '**set_username':
        room.client.info['username'] = data['data']
        room.display_info("username has been set successfully to {}".format(data['data']))
