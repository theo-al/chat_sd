CHAT_ADDR = 'localhost'
CHAT_PORT = 6000

SERV_CHAT = (CHAT_ADDR, CHAT_PORT)

def msg_to_tuple(msg: dict):
    return msg['timestamp'], msg['from'], msg['to'], msg['content']

__all__ = [
    msg_to_tuple.__name__,

    'SERV_CHAT',
]