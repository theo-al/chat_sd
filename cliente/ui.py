import subprocess
import os

from shutil import get_terminal_size

from .. import msg_to_tuple


if os.name == 'nt': 
    def clear_scr():
        subprocess.call('cls', shell=True)
    #! ver se funciona
else:
    clear_scr_seq = subprocess.check_output('clear', shell=True).decode()

    def clear_scr():
        print(clear_scr_seq, end='') 

def move_cursor(x: int, y: int) -> None:
    print(f"\033c[{x};{y}f") #! checar ordem / portabilidade

def render_msg(msg: dict) -> str:
    ts, author, recipient, content = msg_to_tuple(msg)
    return f"[{ts}] {author}: {content}" if not recipient else \
           f"[{ts}] {author} (para você): {content}"

def draw_scr(title: str='chat',
             msgs: list[dict[str, str]]=[],
             extra: str=' ',
             prompt: str='>') -> None:
    sz = get_terminal_size()

    print(title[:sz.columns]) #! não vai aparecer se tiver muita mensagem
    for m in msgs[-sz.lines+3:]: #! descobrir esse 3 com código
        print(render_msg(m)[:sz.columns])
    print(extra[:sz.columns])

    print(prompt[:sz.columns], end=' ', flush=True)
