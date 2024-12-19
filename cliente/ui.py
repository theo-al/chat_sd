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

def draw_scr(title: str='',
             msgs: list[dict[str, str]]=[],
             lines: list[str]=[],
             extra: str=' ',
             prompt: str='>') -> None:
    sz = get_terminal_size()
    max_msgs = sz.lines - len(lines) - 3#! descobrir esse 3 com código

    #! não printar o título/extra se tiverem vazios, aproveitar pra contar linhas extras

    print(title[:sz.columns]) #! não vai aparecer se tiver mensagens longas

    for m in msgs[-max_msgs:]: 
        print(render_msg(m)[:sz.columns])
    for l in lines[:sz.lines]:
        print(l[:sz.columns])

    print(extra[:sz.columns])

    print(prompt[:sz.columns], end=' ', flush=True)

def warn(msg: str):
    draw_scr(extra=msg, prompt='')

def input(prompt='', lines=[], title='', clear=True, queue=None):
    self = input

    if clear: clear_scr()
    draw_scr(
        title=title,
        lines=lines,
        extra=prompt,
    )
    assert self.queue
    return self.queue.get()

input.queue = None #! explicar