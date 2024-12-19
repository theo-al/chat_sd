CHAT_ADDR = 'localhost'
CHAT_PORT = 6000

BIND_ADDR = 'localhost'
BIND_PORT = 6044

SERV_CHAT = (CHAT_ADDR, CHAT_PORT)
SERV_BIND = (BIND_ADDR, BIND_PORT)

def msg_to_tuple(msg: dict):
    return msg['timestamp'], msg['from'], msg['to'], msg['content']

__all__ = [
    msg_to_tuple.__name__,

    'SERV_CHAT',
    'SERV_BIND',
]