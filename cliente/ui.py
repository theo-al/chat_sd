import subprocess

from shutil import get_terminal_size

from .. import msg_to_tuple


## setape
clear_scr_seq = subprocess.check_output('clear', shell=True).decode() #! unix

## funções que mexem com o terminal
def clear_scr():
    print(clear_scr_seq, end='') 

def highlight(s: str):
    return "\033[7m" + s + "\033[0m"


## funções utilitárias
def render_msg(msg: dict, username=None) -> str:
    ts, author, recipient, content = msg_to_tuple(msg)
    _author = author if author != username else author + " (você)"

    if  (recipient is None) or (username is None): 
        ret = f"[{ts}] {_author}: {content}"
    elif recipient == username:
        ret = f"[{ts}] {_author} (para você): {content}" 
    elif author == username:
        ret = f"[{ts}] {_author} para {recipient}: {content}"
    else:
        print(_author, author, recipient, username, content)
        assert False
    
    return ret


## funções de desenhar na tela
def draw_scr(title:  str='',
             msgs:   list[dict]=[],
             lines:  list[str]=[],
             extra:  str=' ',
             prompt: str='>',
             user:   str|None=None) -> None:
    sz = get_terminal_size()

    _title  = title[:sz.columns]
    msgs_   = msgs[-sz.lines:] 
    _lines  = lines[:sz.lines]
    _extra  = extra[:sz.columns]
    _prompt = prompt[:sz.columns]
    
    sz_rest = bool(title) + bool(extra) + bool(prompt)
    max_msgs = sz.lines - len(_lines) - sz_rest

    _msgs = msgs_[-max_msgs:];    

    if _title: print(_title)

    for m in _msgs: 
        print(render_msg(m, username=user)[:sz.columns])
    for l in _lines:
        print(l[:sz.columns])

    if _extra: print(_extra)
    if _prompt:
        print(_prompt, end=' ', flush=True)

def warn(msg: str):
    draw_scr(extra=msg, prompt='')

def input(prompt=' ', lines=[], title='', clear=True, queue=None):
    self = input

    if clear: clear_scr()
    draw_scr(
        title=title,
        lines=lines,
        extra=prompt,
    )
    assert self.queue
    return self.queue.get()

input.queue = None # explicar no vídeo