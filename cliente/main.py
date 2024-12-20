from xmlrpc.client import ServerProxy, Fault

from threading import Thread
from queue     import Queue
from typing    import Never

from . import ui

from .. import BIND_ADDR, BIND_PORT


#! lidar com entrada inválida pro rpc

#! mostrar diferente quando alguém entra na sala
#! parsear args linha de comando
#! fazer funçãozinha pra lidar com line wrap e linhas
#! cores (+- já)


# setape
binder = ServerProxy(f"http://{BIND_ADDR}:{BIND_PORT}", allow_none=True)
CHAT_ADDR, CHAT_PORT = binder.get_addr()
server = ServerProxy(f"http://{CHAT_ADDR}:{CHAT_PORT}", allow_none=True)

username  = None
room_name = None

msgs  = list[dict]()
q     = Queue[str]()

ui.input.queue = q # explicar no vídeo

def connected(): #! colocar no stub do binder aqui do client
    try: server.ping()

    except ConnectionError: return False
    except Exception as e:  return False #! checar
    else:                   return True

def menu(sel: int = 0) -> bool:
    global username, room_name

    options = [
        'iniciar',
        'lista de salas',
        'escolher nome',
        'escolher sala',
        'sair',
    ]
    while True:
        ui.clear_scr()
        menu_screen(options, sel)

        cmd = q.get()
        if not cmd: break

        for c in cmd:
            if c == "n": sel += 1
            if c == "p": sel -= 1
            sel %= len(options)

    selected = options[sel]
    if selected == 'iniciar': return True
    if selected == 'sair':    raise KeyboardInterrupt

    if   selected == 'lista de salas':
        ui.clear_scr()
        ui.input(title='salas disponíveis:',
                 lines=server.list_rooms(),
                 prompt="aperte enter para sair")
    elif selected == 'escolher nome':
        ui.clear_scr()
        username = ui.input("insira seu nome de usuário")
    elif selected == 'escolher sala':
        ui.clear_scr()
        room_name = ui.input(title='salas disponíveis:',
                             prompt="insira nome da sala",
                             lines=server.list_rooms())

    return False
        
def menu_screen(options, selection: int):
    selected = options[selection]
    opt = options.copy() + ['']
    opt[selection] = ui.highlight(selected)
    ui.draw_scr(title="menu",
                lines=opt,
                extra="n/p <enter> para se mover e <enter> para selecionar",
                prompt='')

def register() -> tuple[str, str]:
    ui.clear_scr()
    _username  = username  if username  else \
                 ui.input("insira seu nome de usuário")
    _room_name = room_name if room_name else \
                 ui.input(title='salas disponíveis:',
                          prompt="insira nome da sala",
                          lines=server.list_rooms())
    return _username, _room_name

def join(room_name): #! dar uma mudada
    global username

    ok, err = server.join_room(username, room_name)
    if not ok: #! fazer match
        if   err == 'room':
            ans = ui.input(title="sala inexistente.",
                           prompt=f"deseja criar a nova sala {room_name}? (s/n)") \
                          .strip().casefold()
            if   ans == 's' or ans == 'y' or not ans:
                ok, err = server.create_room(room_name)
                ok, err = server.join_room(username, room_name)
            elif ans == 'n':
                return False, ui.draw_scr(extra="ok", prompt='')
            else:
                return False, ui.draw_scr(extra="por favor tente novamente", prompt='')
        elif err == 'user':
            username = ui.input(title='erro: nome de usuário já em uso.',
                                prompt="digite um novo nome:")
            ok, err = server.join_room(username, room_name)

    if ok: msgs = err
    else:
        ui.draw_scr(title="ocorreu um erro inesperado",
                    extra="por favor tente novamente")
        return False, ()
    
    return True, msgs


def is_cmd(s: str, cmd: str) -> bool:
    s = s.strip().casefold()
    return cmd.startswith(s)

def interpret_command(msg: str, server=server) -> tuple[list, str]: #! melhorar
    global msgs, username, room_name #!

    lines, extra = [], ' '
    if len(msg) <= 1: return lines, extra

    cmd, *args = msg[1:].split()

    if   is_cmd(cmd, 'quit'): raise KeyboardInterrupt
    elif is_cmd(cmd, 'exit'): #!
        server.leave_room(username, room_name)
        while not menu(): pass

        username, room_name = register()
        ok, msgs = join(room_name)
        if not ok:
            raise KeyboardInterrupt
    elif is_cmd(cmd, 'tell'):
        usage = "modo de uso: tell <destino> <mensagem>"
        if args:
            recipient, *rest = args
        else: return lines, usage
 
        msg = ' '.join(rest).strip()
        if msg:
            server.send_message(username, room_name, msg, recipient)
        else: return lines, usage

        extra = f"enviada mensagem privada '{msg}' a {recipient}"
    elif is_cmd(cmd, 'list'):
        users = server.list_users(room_name)
        extra = 'usuários nessa sala: ' + ', '.join(users)
    elif is_cmd(cmd, 'help'):
        lines = [
            ui.highlight('ajuda: comandos disponíveis'),
            "  :quit                      [sai do programa]",
            "  :exit                      [sai da sala]",
            "  :tell <destino> <mensagem> [manda uma mensagem privada]",
            "  :list                      [lista os usuários na sala]"
        ]
    else:
        extra = f"comando inválido: {msg}"

    return lines, extra

def queue_input(queue: Queue) -> Never:
    while True:
        msg = input().strip()
        queue.put(msg)

def main():
    global msgs, username, room_name

    while not menu(): pass

    username, room_name = register()
    ok, msgs = join(room_name)
    if not ok:
        raise KeyboardInterrupt

    clear = True
    lines = []
    extra = "dica: escreva e aperte enter para enviar uma mensagem, " \
            "veja os comandos disponíveis com `:help`"
    while True:
        if not q.empty():
            clear, lines, extra = True, [], ' '

            msg = q.get()
            if   msg.startswith(':'):
                lines, extra = interpret_command(msg)
            elif msg:
                _ = server.send_message(username, room_name, msg)

        new_msgs = server.receive_messages(username, room_name)

        if clear or new_msgs:
            msgs += new_msgs
            ui.clear_scr()
            ui.draw_scr(title=ui.highlight(f'chat da sala {room_name}'),
                        msgs=msgs,
                        lines=lines,
                        extra=extra,
                        prompt=f'{username}>',
                        user=username)

        clear = False


if __name__ == "__main__":
    Thread(name='input_thread', daemon=True,
           target=queue_input, args=[q]).start()

    try: main()

    except ConnectionRefusedError: #! ver
        ui.clear_scr() #! talvez perguntar se tentar de novo
        ui.warn("não foi possível manter a conexão com o servidor")
        ui.warn("saindo do programa")
    except ConnectionError: #! ver
        ui.clear_scr() #! talvez perguntar se tentar de novo
        ui.warn("erro na comunicação com o servidor")
        ui.warn("saindo do programa")
    except Fault as e:
        ui.warn(f"erro {e} no servidor")
        ui.warn("saindo do programa") #! não sair
    except KeyboardInterrupt:
        ui.warn("saindo do programa")
    finally:
        if connected():
            server.leave_room(username, room_name)
