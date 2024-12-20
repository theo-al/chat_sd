from xmlrpc.server import SimpleXMLRPCServer

from .. import SERV_BIND


## configuração inicial
ADDR, PORT = SERV_BIND
SERV_ADDR = None

# rpc
def get_addr():
    while not SERV_ADDR: pass
    return SERV_ADDR

def set_addr(addr):
    global SERV_ADDR
    SERV_ADDR = addr


## programa principal
def main():
    server = SimpleXMLRPCServer((ADDR, PORT), allow_none=True)

    server.register_function(get_addr)
    server.register_function(set_addr)

    print(f"Binder rodando na porta {PORT}...")
    try: server.serve_forever()

    except KeyboardInterrupt:
        print("saindo")

if __name__ == "__main__":
    main()

#! registrar tudo
