from flask import Blueprint,Response,request,jsonify
import mysql.connector
from config import Config
import logging
from utils.sp_handler import search_songs_spotify
from utils.yt_handler_PYTUBE import search_videos_yt
from utils.globalDb import (
    fetch_songs, get_playlistSongs, fetch_User_LikedSongs, fetchTrendingSongs,
    fetchUserTopSongs, get_playlists, fetchStreamRate,createPlaylistDB,updatePlaylistDB
)

import threading
youtube_results = {}
spotify_results = {}
yt_lock = threading.Lock()
sp_lock = threading.Lock()

songs_bp = Blueprint('songs', __name__)



mydb = Config.mydb
mycursor = mydb.cursor()

@songs_bp.route('/gp/<userId>')
def fetchUserTopSongs(userId, limit=10):
    """
    Fetch top songs based on how many times a specific user has viewed them.
    """
    print(f"Fetching top songs for user: {userId}")
    
    useridentity = 'user_id'

    if '@' in userId and '.'  in userId:
        useridentity = 'email'

    try:

        sql_query = f"""
            SELECT 
                s.song_id, 
                s.title, 
                s.artist, 
                s.thumbnail_path AS album_cover, 
                s.release_date,
                v.view_count AS user_view_count
            FROM injustifymusic s
            JOIN views v ON s.song_id = v.song_id
            WHERE v.{useridentity} = %s  -- Change this!
            ORDER BY v.view_count DESC
            LIMIT %s
        """
        values = (userId, limit)

        mycursor.execute(sql_query, values)

        top_songs = mycursor.fetchall()

        # Convert tuples to dictionaries
        top_songs_list = [
            {
                "song_id": song[0],
                "title": song[1],
                "artist": song[2],
                "thumbnail": f'/{song[3]}',  # Corrected variable
                "release_date": song[4].strftime('%Y-%m-%d') if song[4] else None,
                "user_view_count": song[5]
            }
            for song in top_songs
        ]

        return {"success": True, "songs": top_songs_list}

    except mysql.connector.Error as err:
        print(f"Error fetching top songs: {err}")
        return {"success": False, "message": "Failed to fetch top songs!"}


@songs_bp.route('/<user_id>', methods=['GET'])
def return_fetch_songs(user_id):
    search = request.args.get('search', '').strip()  

    if search and search.lower() != "null":
        # Start background threads for YouTube & Spotify searches
        threading.Thread(target=fetch_youtube_results, args=(search,), daemon=True).start()
        threading.Thread(target=fetch_spotify_results, args=(search,), daemon=True).start()


    return jsonify(fetch_songs(user_id, 24, 0 ,search,None))

def fetch_youtube_results(query):
    results = search_videos_yt(query)
    with yt_lock:
        youtube_results[query] = results
    #logging.debug(f"YouTube results saved for query '{query}'")
    #print(f"Current stored YouTube results: {youtube_results.keys()}")  # Debugging

def fetch_spotify_results(query):
    results = search_songs_spotify(query)
    with sp_lock:
        spotify_results[query] = results
    #print(f"Current stored Spotify results: {spotify_results.keys()}")  # Debugging


yt_lock = threading.Lock()
sp_lock = threading.Lock()


@songs_bp.route('pol/yt/<userId>', methods=['GET'])
def get_yt_results(userId):
    search_query = request.args.get('search', '').strip()

    with yt_lock:
        if search_query in youtube_results:
            return jsonify({"success": True, "songs": youtube_results[search_query]})
    
    return jsonify({"success": False, "message": "YouTube results not ready yet"}), 404



@songs_bp.route('/pol/sp/<userId>', methods=['GET'])
def get_sp_results(userId):
    """Returns stored Spotify results for a given query."""
    search_query = request.args.get('search', '').strip()
    
    #print(f"Searching for query in YouTube results: '{search_query}'")  # Debug
    #print(f"Available YouTube result keys: {spotify_results.keys()}")  # Debug

    with sp_lock:
        if search_query in spotify_results:
            return jsonify({"success": True, "songs": spotify_results[search_query]})
    
    return jsonify({"success": False, "message": "Spotify results not ready yet"}), 404

@songs_bp.route('/song/info/<songId>', methods=['GET'])
def fetch_song_info(songId):
    return jsonify(fetch_songs(None, 24, 24, 0 ,songId))






@songs_bp.route('/pl/<pl_id>', methods=['GET'])
def fetch_playlists(pl_id):
    """
    Fetch songs for a playlist with optional search filtering.
    """
  
    if not pl_id:
        return jsonify({"message": "Playlist ID is required"}), 400
    
    print(f"Fetching songs for playlist: {pl_id}")
    pl_songs = get_playlistSongs(pl_id)
    if not pl_songs:
        return jsonify({"message": "Playlist is empty"}), 204
    
    return jsonify({"songs": pl_songs})

@songs_bp.route('/yls/<userId>', methods=['GET'])
def get_User_Liked_songs(userId):
    """
    Fetch songs that a user has liked.
    """

    if not userId:
        return jsonify({"message": "User ID is required"}), 400
        
    liked_songs = fetch_User_LikedSongs(userId,0,20)
    if not liked_songs:
        return jsonify({"message": "No liked songs found",'songs':[]}), 204
    
    return jsonify({"songs": liked_songs.get('feed')}),200

@songs_bp.route('/utr/<userId>', methods=['GET'])
def get_User_Top_songs(userId):
    """
    Fetch songs that a user has streamed the most.
    """
    if not userId:
        return jsonify({"message": "User ID is required"}), 400
        
    songs = fetchUserTopSongs(userId,20)
    if not songs:
        return jsonify({"message": "No liked songs found","songs":[]}), 204
    
    return jsonify({"songs": songs.get('feed')}),200

@songs_bp.route('/tr', methods=['GET'])
def get_Trending_songs():
        
    """
    fetch trending songs.
    """   
    songs = fetchTrendingSongs()
    if not songs:
        return jsonify({"message": "No liked songs found","songs":[]}), 204
    
    return jsonify({"songs": songs.get('feed')}),200

@songs_bp.route('/pls/<userId>', methods=['GET'])
def get_user_playlists(userId):
    """
    Fetch playlists for a user.
    """
    if not userId:
        return jsonify({"message": "User ID is required"}), 400
    
    playlists = get_playlists(userId)
    if not playlists:
        return jsonify({"message": "No playlists found"}), 204
    
    return jsonify({"playlists": playlists.get('playlists')}),200
        
@songs_bp.route('/str/<userId>', methods=['GET'])
def get_Stream_position(userId):
    """
    Fetch playlists for a user.
    """
    if not userId:
        return jsonify({"message": "User ID is required"}), 400
    
    rate = fetchStreamRate(userId)
    #print(f"Fetching stream rate:: {rate}")
    if not rate:
        return jsonify({"message": "No playlists found"}), 204
    
    return jsonify({"stream_rate": rate.get('stream_rate')}),200
        
@songs_bp.route('/add_pls', methods=['POST'])
def createPlaylist():
    data = request.get_json()
    playlistName = data.get('name')
    userId = data.get('userId')

    if not playlistName:
        return jsonify({'error': True, 'message': 'Playlist name CANNOT be empty!!'}), 400

    result = createPlaylistDB(playlistName, userId)

    if result.get('success'):
        return jsonify({
            'success': True,
            'message': result['message'],
            'info': result['info']
        }), 200
    else:
        return jsonify({'error': True, 'message': result['message']}), 500

     



@songs_bp.route('/rnm_pls', methods=['POST'])
def renamePlaylist():
    data = request.get_json()
    playlistId = data.get('playlistId')
    newName = data.get('newName')

    if not newName or not playlistId:  
        return jsonify({'error': True, 'message': 'Playlist ID and name are required!'}), 400

    result = updatePlaylistDB(playlistId, None, 'rename', newName)

    if result.get('success'):  
        return jsonify({
            'success': True,
            'message': result['message'],
            'info': result.get('info', {})  
        }), 200
    else:
        return jsonify({'error': True, 'message': result.get('message', 'Unknown error')}), 500




























from datetime import datetime

def calculate_stream_position(view_history):
    """
    Determines the next song position based on viewing history.
    
    :param view_history: List of dictionaries containing song data
        [{'song_id': 1, 'view_count': 5, 'progress': 80, 'last_viewed': '2025-02-20 14:30:00'}, ...]
    :return: song_id of the next song
    """
    weights = {
        'view_count': 0.5,   # Weight for the number of views
        'progress': 0.3,     # Weight for progress percentage
        'recency': 0.2       # Weight for recency of last view
    }
    
    def time_decay(last_viewed):
        """Calculates time decay factor (more recent = higher value)."""
        now = datetime.now()
        last_viewed_dt = datetime.strptime(last_viewed, '%Y-%m-%d %H:%M:%S')
        delta_days = (now - last_viewed_dt).days + 1  # Avoid division by zero
        return 1 / delta_days  # More recent = higher value
    
    for song in view_history:
        song['recency'] = time_decay(song['last_viewed'])
        song['score'] = (song['view_count'] * weights['view_count'] +
                         song['progress'] * weights['progress'] / 100 +
                         song['recency'] * weights['recency'])
    
    # Sort by score in descending order and return top song_id
    next_song = max(view_history, key=lambda x: x['score'])
    return next_song['song_id']
    































"""
WITH user_activity AS (
    SELECT 
        user_id,
        COUNT(*) AS total_views,
        COUNT(DISTINCT song_id) AS unique_songs,
        AVG(progress) AS avg_completion,
        SUM(view_count) AS total_view_count,
        MAX(last_viewed) AS last_active
    FROM injustify.views
    GROUP BY user_id
), ranking_data AS (
    SELECT 
        user_id,
        total_views,
        unique_songs,
        avg_completion,
        total_view_count,
        -- Apply time decay for recent activity boost
        DATEDIFF(NOW(), last_active) AS days_since_active,
        -- Scoring system
        (total_view_count * 0.5 + unique_songs * 0.3 + avg_completion * 0.2) / (1 + DATEDIFF(NOW(), last_active) * 0.05) AS engagement_score
    FROM user_activity
)
SELECT user_id, 
       RANK() OVER (ORDER BY engagement_score DESC) AS global_rank,
       engagement_score,
       total_views,
       unique_songs,
       avg_completion
FROM ranking_data;

"""    





