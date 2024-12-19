BIND_ADDR = 'localhost'
BIND_PORT = 6044

SERV_BIND = (BIND_ADDR, BIND_PORT)

def msg_to_tuple(msg: dict):
    return msg['timestamp'], msg['from'], msg['to'], msg['content']

__all__ = [
    msg_to_tuple.__name__,

    'SERV_BIND',
]