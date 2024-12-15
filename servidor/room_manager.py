from time   import strftime
from typing import NamedTuple

#! se o usuário não tiver na sala, não deixar enviar mensagem
#! se o usuário já tiver na sala, não deixar entrar

room = NamedTuple('room', [('users', set),
                           ('messages', list)])

rooms = dict[str, room]()
#! ^ apontar como privado?

def create_room(room_name):
    if room_name in rooms:
        return False, "Room already exists."
    rooms[room_name] = room(users=set(),
                            messages=[])
    return True, f"Room '{room_name}' created."

def join_room(username, room_name):
    if room_name not in rooms:
        return False, "Room does not exist."
    rooms[room_name].users.add(username)
    return True, get_past_messages(room_name)

def leave_room(username, room_name):
    if room_name in rooms:
        rooms[room_name].users.discard(username)
        if not rooms[room_name].users:
            del rooms[room_name]

def list_rooms():
    return list(rooms.keys())

def list_users(room_name):
    return list(rooms[room_name].users) \
           if room_name in rooms else []


def add_message(room_name, username, content, recipient=None):
    if room_name not in rooms: return None #! lidar com isso direito

    msg = {
        #! não tou escrevendo se é unicast ou broadcast (mas é redundante)
        "from": username, "to": recipient,
        "content": content,
        "timestamp": strftime("%Y-%m-%d %H:%M:%S"),
    }

    rooms[room_name].messages.append(msg)
    return msg

#! retornar só as mensagens novas
def get_messages(room_name, recipient):
    return [msg for msg in rooms[room_name].messages
            if (msg["to"] == recipient or
                msg["to"] is None)]
    #! usar filter

def get_past_messages(room_name, max_msgs=50):
    result = [msg for msg in rooms[room_name].messages
                if msg["to"] is None]
    #! usar filter
    return result[-max_msgs:] # Retorna as últimas {max_msgs} mensagens


def dump_messages():
    ... #! colocar num 'nome.db' em json ou pickle
def load_messages():
    ... #! puxar de um 'nome.db' em json ou pickle
