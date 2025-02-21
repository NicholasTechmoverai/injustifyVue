from flask import Blueprint,Response,request,jsonify
import mysql.connector
from config import Config
songs_bp = Blueprint('songs', __name__)



mydb = Config.mydb
mycursor = mydb.cursor()

@songs_bp.route('/gp<userId>')
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
def fetch_songs(user_id, songs_per_page=24, offset=0):
    """
    Fetch songs for a user with optional search filtering.
    """
    search_query = request.args.get('search', '').strip()  # ✅ Get search parameter
    offset = int(request.args.get('offset', 0))  # ✅ Get offset (default 0)

    print(f"Fetching songs for user: {user_id} with search query: {search_query}")

    try:
        base_query = """
            SELECT 
                injustifyMusic.song_id, 
                artist, 
                title, 
                url, 
                thumbnail_path, 
                duration, 
                views, 
                upload_date,
                (SELECT COUNT(*) FROM songlikes WHERE songlikes.song_id = injustifyMusic.song_id) AS likes,
                EXISTS(
                    SELECT 1 
                    FROM songlikes 
                    WHERE songlikes.song_id = injustifyMusic.song_id AND songlikes.user_id = %s
                ) AS liked
            FROM injustifyMusic
        """
        values = [user_id]  

        # Search filtering
        if search_query:
            search_filter = f"%{search_query}%"
            count_query = """
                SELECT COUNT(*)
                FROM injustifyMusic
                WHERE title LIKE %s OR artist LIKE %s
            """
            mycursor.execute(count_query, (search_filter, search_filter))
            total_songs = mycursor.fetchone()[0]

            if offset >= total_songs:
                return jsonify({"message": "No results found", "songs": []})

            sql_query = f"""
                {base_query}
                WHERE title LIKE %s OR artist LIKE %s
                ORDER BY title LIMIT %s OFFSET %s
            """
            values.extend([search_filter, search_filter, songs_per_page, offset])

        else:
            # No search query
            count_query = "SELECT COUNT(*) FROM injustifyMusic"
            mycursor.execute(count_query)
            total_songs = mycursor.fetchone()[0]

            if offset >= total_songs:
                return jsonify({"message": "No results found", "songs": []})

            sql_query = f"{base_query} ORDER BY title LIMIT %s OFFSET %s"
            values.extend([songs_per_page, offset])

        mycursor.execute(sql_query, tuple(values))

        # Fetch songs
        songs = mycursor.fetchall()
        result = [
            {
                "song_id": song[0],
                "artist": song[1],
                "title": song[2],
                "url": f'{song[3]}',
                "thumbnail": f"{Config.thumbnailPath}/{song[4]}",
                "duration": song[5],
                "views": song[6],
                "date": song[7].strftime('%Y-%m-%d %H:%M:%S'),
                "likes": song[8],
                "liked": bool(song[9]),  # Convert to boolean
                "Stype": "local"
            }
            for song in songs
        ]

        return jsonify({"total_songs": total_songs, "songs": result})

    except mysql.connector.Error as err:
        print(f"Error fetching songs: {err}")
        return jsonify({"message": "Error fetching songs", "error": str(err)}), 500



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
        

def get_playlistSongs(playlistId):
    sql_query = """
        SELECT ps.song_id, im.title, im.artist, im.url, im.thumbnail_path, p.name 
        FROM playlistSongs ps 
        JOIN injustifyMusic im 
        ON ps.song_id = im.song_id 
        JOIN playlists p 
        ON ps.playlist_id = p.playlist_id 
        WHERE ps.playlist_id = %s;
    """
    values = (playlistId,)
    try:
        mycursor.execute(sql_query, values)
        songs = mycursor.fetchall()

        if not songs:
            return {"playlist_name": None, "songs": []}

        playlist_name = songs[0][5]  # Get the playlist name (same for all songs)
        
        result = [
            {    
                "song_id": song[0],
                "title": song[1],
                "artist": song[2],
                "url": f'{song[3]}',
                "thumbnail": f"{Config.thumbnailPath}/{song[4]}",
                "Stype": "local"
            }
            for song in songs
        ]
        
        return {"playlist_name": playlist_name,"playlistId":playlistId, "songs": result}

    except Exception as e:
        print("Error fetching playlist songs:", str(e))
        return {"playlist_name": None, "songs": []}


def fetchTrendingSongs():
    """
    Fetch trending songs based on views, likes, and comments within the last 30 days.

    Criteria: JUST FOR DEVELOPMENT
    - Songs viewed by at least 5 unique users in the past 30 days.
    - Songs with at least 5 comments in the past 30 days.
    - Songs with engagement ranked by:
      1. Average progress percentage.
      2. Number of likes.
      3. Number of comments.

    """
    print("Fetching trending songs...")

    try:
        sql_query = """
            SELECT 
                s.song_id, 
                s.title, 
                s.artist, 
                s.thumbnail_path,
                s.upload_date, 
                AVG(v.progress) AS average_progress,
                COUNT(DISTINCT l.user_id) AS likes_count,
                COUNT(DISTINCT c.comment_id) AS comments_count
            FROM injustifymusic s
            JOIN views v ON s.song_id = v.song_id
            LEFT JOIN songlikes l ON s.song_id = l.song_id AND l.like_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
            LEFT JOIN comments c ON s.song_id = c.songId AND c.created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
            WHERE v.last_viewed >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
            GROUP BY s.song_id, s.title, s.artist, s.album, s.upload_date
            HAVING COUNT(DISTINCT v.user_id) >= 1 AND COUNT(DISTINCT c.comment_id) >= 1
            ORDER BY average_progress DESC, likes_count DESC, comments_count DESC
        """

        mycursor.execute(sql_query)
        trending_songs = mycursor.fetchall()

        trending_songs_list = []
        for song in trending_songs:
            song_data = {
                'id': song[0],
                'title': song[1],
                'artist': song[2],
                'thumbnail': f"{Config.thumbnailPath}/{song[3]}",
                'upload_date': song[4].strftime('%Y-%m-%d'),
                'average_progress': song[5],
                'likes_count': song[6],
                'comments_count': song[7]
            }
            trending_songs_list.append(song_data)

        return {"success": True, "feed": trending_songs_list}


    except Exception as e:
        print(f"Error fetching trending songs: {e}")
        return []




def fetch_User_LikedSongs(userId, offset=0, limit=10):
    """
    Fetch songs liked by a user, sorted in descending order (recently liked),
    with pagination (10 per fetch by default). Converts tuples to dictionaries.
    """
    print(f"Fetching liked songs for user: {userId}")

    try:
        conn = Config.get_db_connection()
        if not conn:
            return {"success": False, "message": "Database connection failed"}

        sql_query = """
            SELECT 
                s.song_id, 
                s.title, 
                s.artist, 
                s.thumbnail_path AS album_cover, 
                s.release_date, 
                l.like_date
            FROM injustifymusic s
            JOIN songlikes l ON s.song_id = l.song_id
            WHERE l.user_id = %s
            ORDER BY l.like_date DESC
            LIMIT %s OFFSET %s
        """
        values = (userId, limit, offset)

        with conn.cursor() as cursor:
            cursor.execute(sql_query, values)
            liked_songs = cursor.fetchall()

        liked_songs_list = [
            {
                "song_id": song[0],
                "title": song[1],
                "artist": song[2],
                "thumbnail": f'{Config.thumbnailPath}\{song[3]}',
                "release_date": song[4].strftime('%Y-%m-%d') if song[4] else None,
                "like_date": song[5].strftime('%Y-%m-%d %H:%M:%S') if song[5] else None
            }
            for song in liked_songs
        ]

        return {"success": True, "feed": liked_songs_list}

    except mysql.connector.Error as err:
        print(f"Error fetching liked songs: {err}")
        return {"success": False, "message": "Failed to fetch liked songs!"}
    
    finally:
        if conn:
            conn.close()  # Always close the connection


def fetchUserTopSongs(userId, limit=10):
    """
    Fetch top songs based on how many times a specific user has viewed them.
    """
    print(f"Fetching top songs for user: {userId}")

    try:
        conn = Config.get_db_connection()
        if not conn:
            return {"success": False, "message": "Database connection failed"}

        sql_query = """
            SELECT 
                s.song_id, 
                s.title, 
                s.artist, 
                s.thumbnail_path AS album_cover, 
                s.release_date,
                v.view_count AS user_view_count
            FROM injustifymusic s
            JOIN views v ON s.song_id = v.song_id
            WHERE v.user_id = %s
            ORDER BY v.view_count DESC
            LIMIT %s
        """
        values = (userId, limit)

        with conn.cursor() as cursor:
            cursor.execute(sql_query, values)
            top_songs = cursor.fetchall()

        # Convert tuples to dictionaries
        top_songs_list = [
            {
                "song_id": song[0],
                "title": song[1],
                "artist": song[2],
                "thumbnail": f'{Config.thumbnailPath}/{song[3]}',  # Corrected variable
                "release_date": song[4].strftime('%Y-%m-%d') if song[4] else None,
                "user_view_count": song[5]
            }
            for song in top_songs
        ]

        return {"success": True, "feed": top_songs_list}

    except mysql.connector.Error as err:
        print(f"Error fetching top songs: {err}")
        return {"success": False, "message": "Failed to fetch top songs!"}

    finally:
        if conn:
            conn.close()  # Always close the connection

def get_playlists(user_id):
    if not user_id:
        return {
            "success": False,
            "message": "User ID is required"
        }
    
    sql_query = "SELECT playlist_id, name, description, created_by FROM playlists WHERE created_by = %s"
    values = (user_id,)
    mycursor.execute(sql_query, values)
    playlists = mycursor.fetchall()
    if playlists:
        return {
            "success": True,
            "playlists": [
                {
                    "id": playlist[0],
                    "name": playlist[1],
                    "description": playlist[2],
                    "created_by": playlist[3]
                }
                for playlist in playlists
            ]
        }
    return {
        "success": False,
        "message": "No playlists found for this user",
        'playlists': []
    }


def fetchStreamRate(userId):
    """
    Fetch stream rate for 10 users surrounding the given userId, including user info.
    Prevents negative ranking issues.
    """
    print(f"Fetching stream rate for user: {userId}")

    try:
        conn = Config.get_db_connection()
        if not conn:
            return {"success": False, "message": "Database connection failed"}

        sql_query = """
            WITH user_activity AS (
                SELECT 
                    v.user_id,
                    COUNT(*) AS total_views,
                    COUNT(DISTINCT v.song_id) AS unique_songs,
                    AVG(v.progress) AS avg_completion,
                    SUM(v.view_count) AS total_view_count,
                    MAX(v.last_viewed) AS last_active
                FROM injustify.views v
                GROUP BY v.user_id
            ), ranking_data AS (
                SELECT 
                    ua.user_id,
                    ua.total_views,
                    ua.unique_songs,
                    ua.avg_completion,
                    ua.total_view_count,
                    DATEDIFF(NOW(), ua.last_active) AS days_since_active,
                    (ua.total_view_count * 0.5 + ua.unique_songs * 0.3 + ua.avg_completion * 0.2) 
                    / (1 + DATEDIFF(NOW(), ua.last_active) * 0.05) AS engagement_score
                FROM user_activity ua
            ), ranked_users AS (
                SELECT 
                    rd.user_id, 
                    u.name,
                    u.picture,
                    RANK() OVER (ORDER BY rd.engagement_score DESC) AS global_rank,
                    rd.engagement_score,
                    rd.total_views,
                    rd.unique_songs,
                    rd.avg_completion
                FROM ranking_data rd
                JOIN injustify.injustifyusers u ON rd.user_id = u.id
            ), user_position AS (
                SELECT global_rank FROM ranked_users WHERE user_id = %s
            )
            SELECT * FROM ranked_users 
            WHERE global_rank BETWEEN 
                CASE 
                    WHEN (SELECT global_rank FROM user_position) > 5 
                    THEN (SELECT global_rank FROM user_position) - 5 
                    ELSE 1  -- If user is in the top 5, start from rank 1
                END
            AND 
                CASE 
                    WHEN (SELECT global_rank FROM user_position) > 5 
                    THEN (SELECT global_rank FROM user_position) + 5 
                    ELSE (SELECT global_rank FROM user_position) + (5 + (5 - (SELECT global_rank FROM user_position))) 
                    -- This ensures we get 10 users in total by shifting the upper bound higher
                END
            ORDER BY global_rank;

        """

        with conn.cursor() as cursor:
            cursor.execute(sql_query, (userId,))
            stream_rate = cursor.fetchall()

        if stream_rate:
            return {
                "success": True,
                "stream_rate": [
                    {
                        "userId": row[0],
                        "username": row[1],
                        "profile_image_url": f"{Config.profilePath}/{row[2]}",
                        "global_rank": row[3],
                        "engagement_score": row[4],
                        "total_views": row[5],
                        "unique_songs": row[6],
                        "avg_completion": row[7]
                    }
                    for row in stream_rate
                ]
            }
        
        return {"success": True, "stream_rate": []}

    except Exception as e:
        print(f"Error fetching stream rate: {e}")
        return {"success": False, "message": "An error occurred while fetching stream rate"}


    finally:
        if conn:
            conn.close()  # Always close the connection














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





