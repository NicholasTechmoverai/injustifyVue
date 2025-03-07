from flask_socketio import SocketIO
from flask_socketio import Namespace, emit, join_room, leave_room
from utils.globalDb import update_view_count
import logging
from config import Config
import random

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
        print(f"User connected to namespace💯💯: {self.namespace}")

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

    def on_updateViewCount(self, data):
        """
        Handles updating view count received via WebSocket for playing song.
        """
        if not isinstance(data, dict):
            logging.error(f"Invalid data type received: {type(data)}. Expected a dictionary.")
            return    

        # Extract values FIRST
        songId = data.get('songId')
        userId = data.get('userId')
        songPercontage = data.get('progress')

        # Validate after extraction
        if not songId or not userId or songPercontage is None:
            logging.error(f"Missing required data: songId={songId}, userId={userId}, percentage={songPercontage}")
            return
        

        # Call function to update view count
        update_view_count(songId, userId, songPercontage)


    def on_request_image(self):
        images = {
            "1": f"{Config.BACKEND_SERVER}/static/animation_files/1d6cff39a8b9a75245a06b970be123dd.gif",
            "2": f"{Config.BACKEND_SERVER}/static/animation_files/giphy (3).gif",
            "3": f"{Config.BACKEND_SERVER}/static/animation_files/5y4jl6.gif",
            "4": f"{Config.BACKEND_SERVER}/static/animation_files/infinite-the-jackal-rubiks-cube.gif",
            "5": f"{Config.BACKEND_SERVER}/static/animation_files/background-waterfall.gif",
            "6": f"{Config.BACKEND_SERVER}/static/animation_files/wp2757861.webp"
        }
        
        image_url = random.choice(list(images.values()))  # Get a random image
        emit("animatesd_player", {"image": image_url}, broadcast=True)  # Send to frontend
