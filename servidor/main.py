from xmlrpc.server import SimpleXMLRPCServer

from .room_manager    import RoomManager
from .message_manager import MessageManager

from .. import SERV_CHAT


# Configuração inicial
ADDR, PORT = SERV_CHAT

room_manager    = RoomManager()
message_manager = MessageManager()

# Métodos RPC
def create_room(room_name):
    return room_manager.create_room(room_name)

def join_room(username, room_name):
    return room_manager.join_room(username, room_name)


def send_message(username, room_name, content, recipient=None):
    return message_manager.add_message(room_name, username, content, recipient)

def receive_messages(username, room_name):
    return message_manager.get_messages(room_name, recipient=username)


def list_rooms():
    return room_manager.list_rooms()

def list_users(room_name):
    return room_manager.list_users(room_name)


def main(args: list[str]):
    server = SimpleXMLRPCServer((ADDR, PORT), allow_none=True)

    server.register_function(create_room,      "create_room")
    server.register_function(join_room,        "join_room")
    server.register_function(send_message,     "send_message")
    server.register_function(receive_messages, "receive_messages")
    server.register_function(list_rooms,       "list_rooms")
    server.register_function(list_users,       "list_users")

    print(f"Chat server registered and running on port {PORT}...")
    server.serve_forever()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])