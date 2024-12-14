import subprocess

from xmlrpc.client import ServerProxy

from threading import Thread
from queue     import Queue
from time      import sleep

from .. import CHAT_ADDR, CHAT_PORT #! binder

#! fazer comandos para criar sala, sussurar, etc
#! rpc pra sair da sala
#! mover coisas pros lugares certos
#! parsear args linha de comando
#! lidar com entrada inválida pro rpc

# setape
binder = ServerProxy(f"http://{CHAT_ADDR}:{CHAT_PORT}") #! binder

username  = input("Enter your username: ")
room_name = input("Enter the room name: ")

messages = []

_ = binder.create_room(room_name) #! não fazer isso aqui
_ = binder.join_room(username, room_name)

clear_scr_seq = subprocess.check_output('cls||clear',
                                        shell=True).decode()

def clear_scr():
    print(clear_scr_seq, end='')
    # m = 2; print(f"\033[H\033[{m}J", end="")

def move_cursor(x: int, y: int):
    print(f"\033c[{x};{y}f") #! checar ordem / portabilidade


def msg_to_tuple(msg):
    return msg['timestamp'], msg['from'], msg['content']

def print_conversation(msgs: list[dict[str, str]]):
    for m in msgs:
        ts, author, content = msg_to_tuple(m)
        print(f"[{ts}] {author}: {content}")

def msg_eql(a: dict, b: dict):
    return msg_to_tuple(a) == msg_to_tuple(b)

def hist_eql(a: list, b: list):
    if len(a) != len(b): return False
    return all(map(msg_eql, a, b))

def is_cmd(s: str, cmd: str):
    s = s.strip().casefold()
    return cmd.startswith(s)

def queue_input(queue: Queue):
    while True:
        msg = input().strip()
        queue.put(msg)

q = Queue()
Thread(name='input_thread', daemon=True,
       target=queue_input, args=[q]).start()

_ = binder.send_message(username, room_name, '') #! não fazer isso
while True:
    clear = False
    while not q.empty():
        msg = q.get()

        if msg.startswith(':'):
            cmd = msg[1:]

            if   is_cmd(cmd, 'quit'): exit()
            elif is_cmd(cmd, 'exit'):
                assert False, "comando não implementado: exit"
            elif is_cmd(cmd, 'tell'):
                assert False, "comando não implementado: tell"
            else:
                print(f"comando inválido: {msg}")
                sleep(1.1)
        elif msg:
            _ = binder.send_message(username, room_name, msg)
        clear = True

    new_msgs = binder.receive_messages(username, room_name)
    if clear or not hist_eql(new_msgs, messages):
        clear_scr()
        print_conversation(new_msgs)
        print(f'{username}> ', end='', flush=True)
        messages = new_msgs
