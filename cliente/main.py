import subprocess

from xmlrpc.client import ServerProxy

from threading import Thread
from queue     import Queue

from shutil import get_terminal_size

from .. import CHAT_ADDR, CHAT_PORT #! binder


#! mover coisas pros lugares certos
#! lidar com entrada inválida pro rpc
#! lidar com retornos das funções
#! fazer menu principal (com opção de ver e criar salas)
#! fazer main()

#! parsear args linha de comando
#! KeyboardInterrupt
#! fazer funçãozinha pra lidar com line wrap e linhas
#! cores


# setape
binder = ServerProxy(f"http://{CHAT_ADDR}:{CHAT_PORT}", allow_none=True) #! binder

username  = input("Enter your username: ")
room_name = input("Enter the room name: ")

messages = list[dict]()
q        = Queue[str]()
extra    = ''
quit     = False

_ = binder.create_room(room_name) #! não fazer isso aqui
_ = binder.join_room(username, room_name)

clear_scr_seq = subprocess.check_output('cls||clear',
                                        shell=True).decode()
# clear_scr_seq = f"\033[H\033[{2}J"

def clear_scr():
    print(clear_scr_seq, end='') 

def move_cursor(x: int, y: int):
    print(f"\033c[{x};{y}f") #! checar ordem / portabilidade

def msg_to_tuple(msg: dict):
    return msg['timestamp'], msg['from'], msg['to'], msg['content']

def render_msg(msg: dict) -> str:
    ts, author, recipient, content = msg_to_tuple(msg)
    return f"[{ts}] {author}: {content}" if not recipient else \
           f"[{ts}] {author} (para você): {content}"

def draw_scr(title: str='chat',
             msgs: list[dict[str, str]]=[],
             extra: str='\n',
             prompt: str='>'):
    sz = get_terminal_size()

    print(title[:sz.columns]) #! não vai aparecer se tiver muita mensagem
    for m in msgs[-sz.lines+3:]:
        print(render_msg(m)[:sz.columns])
    print(extra[:sz.columns])

    print(prompt[:sz.columns], end=' ', flush=True)

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

Thread(name='input_thread', daemon=True,
       target=queue_input, args=[q]).start()

_ = binder.send_message(username, room_name, '') #! não fazer isso
while not quit:
    clear = False

    while not q.empty():
        extra = ''

        msg = q.get()
        if msg.startswith(':'):
            cmd, *args = msg[1:].split() \
                         if len(msg) > 1 \
                         else (' ', [])

            if   is_cmd(cmd, 'quit'): quit = True
            elif is_cmd(cmd, 'exit'):
                _ = binder.leave_room(username, room_name)
                quit = True #! levar pra um menu
            elif is_cmd(cmd, 'tell'):
                recipient_name, *rest = args
                msg = ' '.join(rest).strip()
                if msg:
                    _ = binder.send_message(username, room_name, msg, recipient_name)
                extra = f"enviada mensagem privada '{msg}' a {recipient_name}"
            else:
                extra = f"comando inválido: {msg}"
        elif msg:
            _ = binder.send_message(username, room_name, msg)

        clear = True

    #! esse if tá aqui pq quando a gente dava exit:
        # 1. a sala é deletada imediatamente
        # 2. sai do programa só depois que o while checa o quit
        # 3. falta um check no servidor
    if not quit:
        new_msgs = binder.receive_messages(username, room_name)

        if clear or not hist_eql(new_msgs, messages):
            clear_scr()
            draw_scr(title=f'chat da sala {room_name}',
                    msgs=new_msgs,
                    extra=extra,
                    prompt=f'{username}>')
            messages = new_msgs

_ = binder.leave_room(username, room_name) #! fazer só se não tiver saído
