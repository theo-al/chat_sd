import xmlrpc.client

from .. import CHAT_ADDR, CHAT_PORT #! binder

# Conexão com o Binder
binder = xmlrpc.client.ServerProxy(f"http://{CHAT_ADDR}:{CHAT_PORT}") #! binder

username  = input("Enter your username: ")
room_name = input("Enter the room name: ")

_ = binder.create_room(room_name) #! não fazer isso aqui
_ = binder.join_room(username, room_name)

#! fazer threads pra pegar as mensagens enquanto não escreve
#! fazer TUIzinha pra janela de chat
#! fazer comandos para criar sala, whisperar, etc
#! rpc pra sair da sala
while True: 
    msg = input("Message (type ':quit' to quit): ").strip()
    if msg.startswith(':'):
        msg = msg[1:].strip().casefold()
        if msg in ('quit', 'q'): break

        print(f"comando! {msg}")
        continue

    _ = binder.send_message(username, room_name, msg)
    messages = binder.receive_messages(username, room_name)
    for m in messages:
        print(f"[{m['timestamp']}] {m['from']}: {m['content']}")
