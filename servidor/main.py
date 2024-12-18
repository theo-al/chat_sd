from xmlrpc.server import SimpleXMLRPCServer

from .  import room_manager
from .. import SERV_CHAT

# configuração inicial
ADDR, PORT = SERV_CHAT

# wrappers rpc que mudam assinatura
def send_message(username, room_name, content, recipient=None):
    return room_manager.add_message(room_name, username, content, recipient)

def receive_messages(username, room_name):
    return room_manager.get_messages(room_name, recipient=username)

# função para checar conexão com o servidor
def ping(): return "pong"


def main():
    server = SimpleXMLRPCServer((ADDR, PORT), allow_none=True)

    server.register_function(room_manager.create_room)
    server.register_function(room_manager.join_room)
    server.register_function(room_manager.leave_room)
    server.register_function(room_manager.list_rooms)
    server.register_function(room_manager.list_users)

    server.register_function(send_message)
    server.register_function(receive_messages)

    server.register_function(ping)

    print(f"Servidor rodando na porta {PORT}...")
    try: server.serve_forever()

    except KeyboardInterrupt:
        print("saindo")

if __name__ == "__main__":
    main()
