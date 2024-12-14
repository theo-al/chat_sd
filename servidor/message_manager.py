import time

class MessageManager:
    def __init__(self):
        self.history = dict() # Listas globais de mensagens para cada sala

    def add_message(self, room_name, username, content, recipient=None):
        if room_name not in self.history:
            self.history[room_name] = []

        msg = {
            "from": username, "to": recipient,
            "content": content,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.history[room_name].append(msg)
        return msg

    def get_messages(self, room_name, recipient=None, max_msgs=50):
        result = [msg for msg in self.history[room_name]
                  if (msg["to"] == recipient or msg["to"] is None)]
        #! não remandar mensagens privadas, fazer métodos diferentes pra isso
        return result[-max_msgs:] # Retorna as últimas {max_msgs} mensagens
