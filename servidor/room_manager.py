import threading


class RoomManager:
    def __init__(self):
        self.rooms = {}  # {room_name: {'users': set(), 'messages': []}}
        self.lock = threading.Lock()

    def create_room(self, room_name):
        with self.lock:
            if room_name in self.rooms:
                return False, "Room already exists."
            self.rooms[room_name] = {'users': set(), 'messages': []}
            return True, f"Room '{room_name}' created."

    def join_room(self, username, room_name):
        with self.lock:
            if room_name not in self.rooms:
                return False, "Room does not exist."
            self.rooms[room_name]['users'].add(username)
            return True, list(self.rooms[room_name]['users'])

    def leave_room(self, username, room_name):
        with self.lock:
            if room_name in self.rooms:
                self.rooms[room_name]['users'].discard(username)
                if not self.rooms[room_name]['users']:
                    del self.rooms[room_name]

    def list_rooms(self):
        return list(self.rooms.keys())

    def list_users(self, room_name):
        return list(self.rooms[room_name]['users']) if room_name in self.rooms else []
