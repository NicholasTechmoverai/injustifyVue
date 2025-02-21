from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

import os
import logging
from config import Config
from websocket_service import INJUserNamespace

from routes.main import main_bp

from routes.profile import profile_bp
from routes.downloads import downloads_bp
from routes.notifications import notifications_bp
from routes.globalp import global_bp
from routes.history import history_bp
from routes.songs import songs_bp

app = Flask(__name__, template_folder="templates", static_folder="static")

app.config['SECRET_KEY'] = Config.SECRET_KEY or "default_secret_key"
app.config['DOWNLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'downloads')
app.config.from_object(Config)


app.config.from_object('config.Config')

from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing

# Enable CORS for Flask-SocketIO
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')


socketio.on_namespace(INJUserNamespace('/user'))

# Register blueprints
app.register_blueprint(main_bp, url_prefix='/api')
app.register_blueprint(profile_bp, url_prefix='/api/profile')
app.register_blueprint(downloads_bp, url_prefix='/api/downloads')
app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
app.register_blueprint(global_bp, url_prefix='/global')
app.register_blueprint(history_bp, url_prefix='/api/history')
app.register_blueprint(songs_bp, url_prefix='/api/songs')

if __name__ == '__main__':
    socketio.run(app, debug=True)
