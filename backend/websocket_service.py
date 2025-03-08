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
            "6": f"{Config.BACKEND_SERVER}/static/animation_files/wp2757861.webp",
            "7": f"{Config.BACKEND_SERVER}/static/animation_files/b20e20379e0def016644ab0b4cc1ebda.gif",
            "8": f"{Config.BACKEND_SERVER}/static/animation_files/tumblr_mn394hFgMI1rasznao1_500.gif",
            "9": f"{Config.BACKEND_SERVER}/static/animation_files/tenor (1).gif",
            "10": f"{Config.BACKEND_SERVER}/static/animation_files/tenor (2).gif",
            "11": f"{Config.BACKEND_SERVER}/static/animation_files/tenor (3).gif",
            "12": f"{Config.BACKEND_SERVER}/static/animation_files/pixel-jeff-galaxy-far-far-away.gif",
            "13": f"{Config.BACKEND_SERVER}/static/animation_files/jackal-running.gif",
            "14": f"{Config.BACKEND_SERVER}/static/animation_files/infinite-the-jackal-fnf-vs-infinite.gif",
            "15": f"{Config.BACKEND_SERVER}/static/animation_files/infinite-loop-anime-girl.gif",
            "16": f"{Config.BACKEND_SERVER}/static/animation_files/icegif-944.gif",
            "17": f"{Config.BACKEND_SERVER}/static/animation_files/Gif-Animated-Wallpaper-Background-Full-HD-Free-Download-for-PC-Macbook-261121-Wallpaperxyz.com-19.webp",
            "18": f"{Config.BACKEND_SERVER}/static/animation_files/demon-slayer.gif",
            "19": f"{Config.BACKEND_SERVER}/static/animation_files/demon-slayer-kimetsu-no-yaiba.gif",
            "20": f"{Config.BACKEND_SERVER}/static/animation_files/dark-mode image.jpg",
            "21": f"{Config.BACKEND_SERVER}/static/animation_files/anime-gif-thunder.gif",
            "22": f"{Config.BACKEND_SERVER}/static/animation_files/16110235550769308128.gif",
            "23": f"{Config.BACKEND_SERVER}/static/animation_files/1479838616hx01_2.gif",
            "24": f"{Config.BACKEND_SERVER}/static/animation_files/62f2ccde1b2fffb43f05ce2e8219cc35.gif",
            "25": f"{Config.BACKEND_SERVER}/static/animation_files/772a6ea88ccedb26a196ab3ff4d57af2.gif",
            "26": f"{Config.BACKEND_SERVER}/static/animation_files/wp2757868.webp",
            "27": f"{Config.BACKEND_SERVER}/static/animation_files/869910.webp",
            "28": f"{Config.BACKEND_SERVER}/static/animation_files/23-24-59-615_512.webp",
            "29": f"{Config.BACKEND_SERVER}/static/animation_files/23f3cf8ba3737bf0145f8d8baec1e9b1.gif",
            "30": f"{Config.BACKEND_SERVER}/static/animation_files/WMZD_hxsTTVz4NCrnM0tOJP81MSPnwMTLVavevaLNhk.gif",
            "31": f"{Config.BACKEND_SERVER}/static/animation_files/R (1).gif",
            "32": f"{Config.BACKEND_SERVER}/static/animation_files/R.gif",
            "33": f"{Config.BACKEND_SERVER}/static/animation_files/giphy (8).gif",
            "34": f"{Config.BACKEND_SERVER}/static/animation_files/giphy.gif",
            "35": f"{Config.BACKEND_SERVER}/static/animation_files/215948.gif",
        }

        image_url = random.choice(list(images.values()))  
        emit("animatesd_player", {"image": image_url}, broadcast=False) 
