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
