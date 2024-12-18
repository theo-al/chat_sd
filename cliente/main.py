from xmlrpc.client import ServerProxy

from threading import Thread
from queue     import Queue
from typing    import Never

from . import ui

from .. import CHAT_ADDR, CHAT_PORT #! binder
from .. import msg_to_tuple


#! lidar com entrada inválida pro rpc
#! lidar com retornos das funções
#! fazer menu principal (com opção de ver e criar salas)
#! fazer uma thread buscadora de mensagem

#! mostrar diferente quando alguém entra na sala
#! parsear args linha de comando
#! fazer funçãozinha pra lidar com line wrap e linhas
#! cores
#! fazer comando help pra saber opções


# setape
binder = ServerProxy(f"http://{CHAT_ADDR}:{CHAT_PORT}", allow_none=True) #! binder

connected = True
msgs  = list[dict]()
q     = Queue[str]()
extra = 'dica: escreva e aperte enter para enviar uma mensagem, ' \
        'veja os comandos disponíveis com :help' #! ainda não tá assim

def msg_eql(a: dict, b: dict) -> bool:
    return msg_to_tuple(a) == msg_to_tuple(b)

def hist_eql(a: list, b: list) -> bool:
    if len(a) != len(b): return False
    return all(map(msg_eql, a, b))

def is_cmd(s: str, cmd: str) -> bool:
    s = s.strip().casefold()
    return cmd.startswith(s)

def queue_input(queue: Queue) -> Never:
    while True:
        msg = input().strip()
        queue.put(msg)

def interpret_command(msg: str, extra='') -> str:
    if len(msg) > 1:
        cmd, *args = msg[1:].split()
    else: return extra

    if   is_cmd(cmd, 'quit'): raise KeyboardInterrupt # rsrsrs
    elif is_cmd(cmd, 'exit'):
        raise KeyboardInterrupt
        #! tamo fazendo igual o quit, sair da sala levar pra um menu em vez disso

    elif is_cmd(cmd, 'tell'):
        uso = "modo de uso: tell <destino> <mensagem>"
        if args:
            recipient, *rest = args
        else: return uso
 
        msg = ' '.join(rest).strip()
        if msg:
            _ = binder.send_message(username, room_name, msg, recipient)
        else: return uso

        extra = f"enviada mensagem privada '{msg}' a {recipient}"
    elif is_cmd(cmd, 'list'):
        users = binder.list_users(room_name)
        extra = 'usuários nessa sala: ' + ', '.join(users)
    else:
        extra = f"comando inválido: {msg}"

    return extra

def main():
    global clear, extra, msgs
    global username, room_name

    _ = binder.create_room(room_name) #! não fazer isso aqui
    _ = binder.join_room(username, room_name)

    _ = binder.send_message(username, room_name, '') #! não fazer isso

    while True:
        clear = False

        if not q.empty():
            clear, extra = True, ''

            msg = q.get()
            if   msg.startswith(':'):
                extra = interpret_command(msg)
            elif msg:
                _ = binder.send_message(username, room_name, msg)

        new_msgs = binder.receive_messages(username, room_name)

        if clear or not hist_eql(new_msgs, msgs):
            ui.clear_scr()
            ui.draw_scr(title=f'chat da sala {room_name}',
                        msgs=new_msgs,
                        extra=extra,
                        prompt=f'{username}>')
            msgs = new_msgs


if __name__ == "__main__":
    username  = input("insira seu nome de usuário: ") #! pegar da thread de input(por dentro da main)?
    room_name = input("insira nome da sala: ") #! pegar da thread de input(por dentro da main)?

    Thread(name='input_thread', daemon=True,
           target=queue_input, args=[q]).start()

    try: main()
    except KeyboardInterrupt:
        ui.clear_scr() #! talvez mostrar um menuzinho
        print("saindo do programa")
    except ConnectionRefusedError: #! ver
        ui.clear_scr() #! talvez perguntar se tentar de novo
        print("não foi possível manter a conexão com o servidor")
        connected = False
    except ConnectionError: #! ver
        ui.clear_scr() #! talvez perguntar se tentar de novo
        print("erro na comunicação com o servidor")
        connected = False
    finally:
        if connected:
            _ = binder.leave_room(username, room_name) #! fazer só se não tiver saído
