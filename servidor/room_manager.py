from time   import strftime
from typing import NamedTuple


room = NamedTuple('room', [('users',    dict[str, dict]),
                           ('messages', list[dict])])

rooms = dict[str, room]()
#! ^ apontar como privado?

def curr_time_str():
    return strftime("%Y-%m-%d %H:%M:%S")

def create_room(room_name):
    if room_name in rooms: return False, "room"

    rooms[room_name] = room(users=dict(),
                            messages=[{
                                "from": None, "to": None,
                                "content": f"bem vindo à sala {room_name}",
                                "timestamp": curr_time_str(),
                            }])
    return True, ()

def get_all_users(): #! deve ser devagar
    return set().union(*(r.users.keys() for r in rooms.values()))

def join_room(username, room_name):
    if room_name not in rooms:
        return False, "room"
    if username in get_all_users():
        return False, "user"

    rooms[room_name].users[username] = len(rooms[room_name].messages) - 1
    return True, get_past_messages(room_name)

def leave_room(username, room_name):
    if room_name in rooms:
        rooms[room_name].users.pop(username)
        if not rooms[room_name].users:
            del rooms[room_name]

def list_rooms():
    return list(rooms.keys())

def list_users(room_name):
    return list(rooms[room_name].users.keys()) \
           if room_name in rooms else []

def add_message(room_name, username, content, recipient=None):
    if (room_name not in rooms) or \
       (username  not in rooms[room_name].users.keys()): return None #! lidar com isso direito

    msg = {
        #! não tou escrevendo se é unicast ou broadcast (mas é redundante)
        "from": username, "to": recipient,
        "content": content,
        "timestamp": curr_time_str(),
    }

    rooms[room_name].messages.append(msg)
    return True #! retornar False se não for válido de alguma forma
    #! checar se tem requisito sobre isso no enunciado

def get_messages(room_name, recipient):
    #! if recipient not in room[room_name].users.keys(): return [] #! lidar com isso direito

    last_msg = rooms[room_name].users[recipient]
    next_idx = last_msg + 1

    msgs = list(filter(lambda msg: (msg["to"]   == recipient or
                                    msg['from'] == recipient or
                                    msg["to"] is None),
                rooms[room_name].messages[next_idx:])) #! checar se duplica
    
    if msgs: rooms[room_name].users[recipient] = len(rooms[room_name].messages) - 1

    return msgs

def get_past_messages(room_name, max_msgs=50):
    result = [msg for msg in rooms[room_name].messages
                  if msg["to"] is None]
    #! usar filter
    return result[-max_msgs:] # Retorna as últimas {max_msgs} mensagens


def dump_messages():
    ... #! colocar num 'nome.db' em json ou pickle
def load_messages():
    ... #! puxar de um 'nome.db' em json ou pickle
