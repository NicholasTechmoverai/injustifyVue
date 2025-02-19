from flask_socketio import SocketIO
from flask_socketio import Namespace, emit, join_room, leave_room


class INJUserNamespace(Namespace):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.username = None

    def on_fetchNoty(self, data):
        """Handle 'fetch/noty' event emitted by the client."""
        
        songId = data.get('songId', 0)
        Notytype = data.get('type', "")

        if not songId:
            return emit('thisNoty', []) 

        your_notifications = []
        emit('thisNoty', {'your_notifications': your_notifications, 'Notytype': Notytype})

    def on_connect(self):
        """Handle a new connection."""
        print(f"User connected to namespace: {self.namespace}")

    def on_disconnect(self):
        """Handle user disconnect."""
        print(f"User disconnected from namespace: {self.namespace}")
        if self.username:
            print(f'{self.username} disconnected')

    def on_loginUser(self, data):
        """Handle user identification."""
        self.username = data.get('userLoggedEmail', '')
        print(f"User {self.username} logged in.")
        emit('message', {'msg': f"Hello {self.username}, welcome!", 'msg_type': 'SUCCESS'})

    def on_message(self, msg):
        """Handle incoming messages."""
        if self.username:
            print(f"Message from {self.username}: {msg}")
            emit('message', {'msg': f"{self.username} said: {msg}"})
        else:
            print(f"Message from unknown user: {msg}")
            emit('message', {'msg': "You need to log in first."})
