from time   import strftime
from typing import NamedTuple

from threading import Timer


## tipos e constantes
room = NamedTuple('room', [('users',    dict[str, dict]),
                           ('messages', list[dict]),
                           ('timer',    Timer | None)])

rooms = dict[str, room]()

MAX_INACTIVE_TIME = 5*60


## funções utilitárias
def curr_time() -> str:
    return strftime("%Y-%m-%d %H:%M:%S")

def get_all_users() -> set[str]: #! deve ser devagar
    return {"SERVIDOR"}.union(*(r.users.keys() for r in rooms.values()))

def user_in_room(username: str, room_name: str) -> bool: #! deve ser devagar
    return (username in rooms[room_name].users.keys()) or \
           (username == "SERVIDOR")

def room_exists(room_name: str) -> bool:
    return room_name in rooms

def user_exists(username: str) -> bool:
    return username in get_all_users()

def get_past_messages(room_name: str, max_msgs=50):
    result = [msg for msg in rooms[room_name].messages
                  if msg["to"] is None]
    return result[-max_msgs:] # retorna as últimas {max_msgs} mensagens


## funções pedidas simples
def list_rooms() -> list[str]:
    return list(rooms.keys())

def list_users(room_name: str) -> list[str]:
    return list(rooms[room_name].users.keys()) \
           if room_name in rooms else []


## resto das funções pedidas
def create_room(room_name: str) -> tuple[bool, str]:
    if room_exists(room_name): return False, "room"

    rooms[room_name] = room(users=dict(),
                            messages=[{
                                "from": "SERVIDOR", "to": None,
                                "content": f"bem vindo à sala {room_name}",
                                "timestamp": curr_time(),
                            }], 
                            timer=None)
    return True, ""

def join_room(username: str, room_name: str):
    if not room_exists(room_name): return False, "room"
    if     user_exists(username):  return False, "user"

    add_message(room_name, "SERVIDOR", f"{username} entrou na sala") #!

    if rooms[room_name].timer:
        rooms[room_name].timer.cancel()
        rooms[room_name] = \
        rooms[room_name]._replace(timer=None)

    rooms[room_name].users[username] = len(rooms[room_name].messages) - 1
    return True, get_past_messages(room_name)

def leave_room(username: str, room_name: str):
    if room_exists(room_name) and user_exists(username):
        rooms[room_name].users.pop(username)
        if not rooms[room_name].users:
            timer = Timer(MAX_INACTIVE_TIME,
                          lambda: rooms.pop(room_name))
            rooms[room_name] = \
            rooms[room_name]._replace(timer=timer)

            timer.start()

def add_message(room_name: str, username: str, content: str, recipient=None):
    if (not room_exists(room_name)) or \
       (not user_in_room(username, room_name)): return False #! lidar com isso direito
    #! retornar tipo de erro

    msg = {
        #! não tou escrevendo se é unicast ou broadcast (mas é redundante)
        "from": username, "to": recipient,
        "content": content,
        "timestamp": curr_time(),
    }

    rooms[room_name].messages.append(msg)
    return True

def get_messages(room_name: str, recipient: str):
    #! if not user_in_room(recipient, room_name): return [] #! lidar com isso direito

    last_msg = rooms[room_name].users[recipient]
    next_idx = last_msg + 1

    msgs = list(filter(lambda msg: (msg["to"]   == recipient or
                                    msg['from'] == recipient or
                                    msg["to"]   is None),
                rooms[room_name].messages[next_idx:])) #! checar se duplica
    
    if msgs: rooms[room_name].users[recipient] = len(rooms[room_name].messages) - 1

    return msgs

#! x._replace(...) -> replace(x, ...)
