import time

class RoomManager:
    def __init__(self):
        # Listas globais de mensagens e usuários para cada sala
        self.rooms = dict()

    def create_room(self, room_name):
        if room_name in self.rooms:
            return False, "Room already exists."
        self.rooms[room_name] = {'users': set(), 'messages': []}
        return True, f"Room '{room_name}' created."

    def join_room(self, username, room_name):
        if room_name not in self.rooms:
            return False, "Room does not exist."
        self.rooms[room_name]['users'].add(username)
        return True, list(self.rooms[room_name]['users'])

    def leave_room(self, username, room_name):
        if room_name in self.rooms:
            self.rooms[room_name]['users'].discard(username)
            if not self.rooms[room_name]['users']:
                del self.rooms[room_name]

    def list_rooms(self):
        return list(self.rooms.keys())

    def list_users(self, room_name):
        return list(self.rooms[room_name]['users']) if room_name in self.rooms else []


    def add_message(self, room_name, username, content, recipient=None):
        if room_name not in self.rooms: return None #! lidar com isso direito

        msg = {
            #! não tou escrevendo se é unicast ou broadcast (mas é redundante)
            "from": username, "to": recipient,
            "content": content,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.rooms[room_name]['messages'].append(msg)
        return msg

    #! retornar só as mensagens novas
    def get_messages(self, room_name, recipient):
        return [msg for msg in self.rooms[room_name]['messages']
                if (msg["to"] == recipient or
                    msg["to"] is None)]
        #! usar filter

    #! usar
    def get_past_messages(self, room_name, max_msgs=50):
        result = [msg for msg in self.rooms[room_name]['messages']
                  if msg["to"] is None]
        #! usar filter
        return result[-max_msgs:] # Retorna as últimas {max_msgs} mensagens


    def dump_messages(self):
        ... #! colocar num 'nome.db' em json ou pickle
    def load_messages(self):
        ... #! puxar de um 'nome.db' em json ou pickle
