import logging
import uuid
import mysql.connector
from config import Config
logging.basicConfig(level=logging.INFO)
from config import Config

mydb = Config.mydb
mycursor = mydb.cursor()

def update_view_count(songId, userId, songPercentage):
    """
    Function to update the view count for a song effectively.
    """
    #logging.info(f"Updating view count for song {songId} by user {userId} with progress {songPercentage}")
    try:
        # Fetch previous data to check wheather a fresh playthrough is required
        sql_check = "SELECT id, view_count, progress FROM views WHERE song_id = %s AND user_id = %s"
        mycursor.execute(sql_check, (songId, userId))
        existing_view = mycursor.fetchone() 

        if existing_view:
            view_id, view_count, last_progress = existing_view

            if last_progress >= 98 and songPercentage < 10:
                # Reset progress tracking for a fresh playthrough
                sql_reset_progress = """
                    UPDATE views 
                    SET progress = %s, last_viewed = NOW()
                    WHERE song_id = %s AND user_id = %s
                """
                mycursor.execute(sql_reset_progress, (songPercentage, songId, userId))

            elif last_progress < 50 and songPercentage >= 50:
                #Increment view count if crossing 50% in a new session
                sql_update_view = """
                    UPDATE views 
                    SET progress = %s, view_count = view_count + 1, last_viewed = NOW()
                    WHERE song_id = %s AND user_id = %s
                """
                mycursor.execute(sql_update_view, (songPercentage, songId, userId))

            else:
                # Just update progress without affecting view count
                sql_update_progress = """
                    UPDATE views 
                    SET progress = %s, last_viewed = NOW()
                    WHERE song_id = %s AND user_id = %s
                """
                mycursor.execute(sql_update_progress, (songPercentage, songId, userId))

        else:
            # First-time entry: insert new record
            viewCount = 1 if songPercentage >= 50 else 0
            sql_insert = """
                INSERT INTO views (user_id, song_id, view_count, progress) 
                VALUES (%s, %s, %s, %s)
            """
            mycursor.execute(sql_insert, (userId, songId, viewCount, songPercentage))

        mydb.commit()  

    except Exception as err:
        print(f"Error updating view count: {err}")

    finally:
        mycursor.fetchall() 



def insert_download(user_id, song_id, file_name, file_format, itag, file_size, file_source, thumbnail, user_agent=None, is_partial=False):
    """Insert a new download into the database."""
    try:
        query = (
            "INSERT INTO downloads (user_id, song_id, file_name, file_format, itag, file_size, file_source, thumbnail, user_agent, is_partial) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        values = (user_id, song_id, file_name, file_format, itag, file_size, file_source, thumbnail, user_agent, is_partial)
        mycursor.execute(query, values)
        mydb.commit()

        print("Download inserted successfully!")
        return mycursor.lastrowid

    except Exception as e:
        print(f"Error inserting download: {e}")
        return None





def fetch_songs(user_id=None, songs_per_page=15, offset=0, search=None,songId=None):
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
        values = [user_id] if user_id else [None]

        if not search or search.lower() == 'null' and not songId:
            # Count total songs without search
            count_query = "SELECT COUNT(*) FROM injustifyMusic"
            mycursor.execute(count_query)
            total_songs = mycursor.fetchone()[0]

            if offset >= total_songs:
                return {"message": "No results found"}

            # Paginated songs query without search
            sql_query = f"{base_query} ORDER BY title LIMIT %s OFFSET %s"
            values.extend([songs_per_page, offset])
            mycursor.execute(sql_query, tuple(values))

          # Fetch songs with songId
        elif songId and not search:
        
            sql_query = f"""
                {base_query}
                WHERE song_id = %s
                ORDER BY title
                LIMIT %s OFFSET %s
                """
            values.extend([songId, songs_per_page, offset])
            mycursor.execute(sql_query, tuple(values))  


         # Fetch songs with search   
        else:
     
            count_query = """
                SELECT COUNT(*)
                FROM injustifyMusic
                WHERE title LIKE %s OR artist LIKE %s
            """
            search_filter = f"%{search}%"
            mycursor.execute(count_query, (search_filter, search_filter))
            total_songs = mycursor.fetchone()[0]

            if offset >= total_songs:
                return {"message": "No results found"}

            # Paginated songs query with search
            sql_query = f"""
                {base_query}
                WHERE title LIKE %s OR artist LIKE %s
                ORDER BY title LIMIT %s OFFSET %s
            """
            values.extend([search_filter, search_filter, songs_per_page, offset])
            mycursor.execute(sql_query, tuple(values))

        # Fetch songs
        songs = mycursor.fetchall()
        result = [
            {
                "song_id": song[0],
                "artist": song[1],
                "title": song[2],
                "url": f'{song[3]}',
                "thumbnail":f"{Config.thumbnailPath}/{song[4]}",
                "duration": song[5],
                "views": song[6],
                "date": song[7].strftime('%Y-%m-%d %H:%M:%S'),
                "likes": song[8],
                "liked": bool(song[9]),  # Convert to boolean
                "Stype": "local"
            }
            for song in songs
        ]

        return {"total_songs": total_songs, "songs": result}

    except mysql.connector.Error as err:
        return {"message": "Error fetching songs", "error": str(err)}


        

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

    try:
        sql_query = """
            SELECT 
                p.playlist_id, 
                p.name, 
                p.description, 
                p.created_by, 
                p.created_at, 
                u.Picture, 
                (SELECT COUNT(*) FROM playlistsongs WHERE playlist_id = p.playlist_id) AS song_count
            FROM playlists p
            LEFT JOIN injustifyusers u ON p.created_by = u.id
            WHERE p.created_by = %s
        """

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
                        "created_by": playlist[3],
                        "created_at": playlist[4].strftime('%Y-%m-%d %H:%M:%S'),
                        "picture": f"{Config.profilePath}/{playlist[5]}",
                        "song_count": playlist[6]
                    }
                    for playlist in playlists
                ]
            }
        return {
            "success": False,
            "message": "No playlists found for this user",
            "playlists": []
        }

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return {
            "success": False,
            "message": "An error occurred while fetching playlists",
            "error": str(err)
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


def createPlaylistDB(playlistName, userId):
    print("Creating playlist " + playlistName + " with user " + userId)
    id = f"pl{str(uuid.uuid4())[:8]}"  # Generate a unique ID and truncate to 8 characters

    sql_query = "INSERT INTO playlists (playlist_id, name, created_by) VALUES (%s, %s, %s)"
    values = (id, playlistName, userId)

    try:
        mycursor.execute(sql_query, values)
        mydb.commit() 
        info = {
            'id': id,
            'playlistName': playlistName,
            'created_by': userId,
            'type': 'local'  
        }

        return {
            'success': True,
            'message': 'Playlist was successfully created😊',
            'info': info
           
        }

    except mysql.connector.Error as err:
        print(f"Error creating playlist: {err}")
        return {
            'success': False,
            'message': 'Error creating playlist!!'
        }


def updatePlaylistDB(playlistId, songId, action,newPlaylistName = None):
    print("Updating playlist", playlistId, " songId  💯💯", songId, "action" , action , "newPlaylistName" , newPlaylistName)

    if action == "add":
        sql_query = "INSERT INTO playlistSongs (playlist_id, song_id) VALUES (%s, %s)"
        values = (playlistId, songId)
        try:
            mycursor.execute(sql_query, values)
            mydb.commit()
            return {
                "success": True,
                "message": "Song added to playlist successfully!"
            }
        except mysql.connector.Error as err:
            print(f"Error adding song to playlist: {err}")
            return {
                "success": False,
                "message": "Failed to add song to playlist!"
            }

    if action == "remove":
        sql_query = "DELETE FROM playlistSongs WHERE playlist_id = %s AND song_id = %s"
        values = (playlistId, songId)

        try:
            mycursor.execute(sql_query, values)
            mydb.commit()
            return {
                "success": True,
                "message": "Song removed from playlist successfully!"
            }
        except mysql.connector.Error as err:
            print(f"Error removing song from playlist: {err}")
            return {
                "success": False,
                "message": "Failed to remove song from playlist!"
            }

    if action == "delete":
        try:
            # Delete related records in playlistsongs
            delete_songs_query = "DELETE FROM playlistsongs WHERE playlist_id = %s"
            mycursor.execute(delete_songs_query, (playlistId,))

            # Delete playlist
            delete_playlist_query = "DELETE FROM playlists WHERE playlist_id = %s"
            mycursor.execute(delete_playlist_query, (playlistId,))

            mydb.commit()
            return {
                "success": True,
                "message": "Playlist deleted successfully!"
            }
        except mysql.connector.Error as err:
            print(f"Error deleting playlist: {err}")
            return {
                "success": False,
                "message": "Failed to delete playlist!"
            }

        
    if action == 'rename':
        if newPlaylistName is not None and newPlaylistName != 'null':
            sql_query = "UPDATE playlists SET name = %s WHERE playlist_id = %s"
            values = (newPlaylistName, playlistId) 

            try:
                mycursor.execute(sql_query, values)
                mydb.commit()
                return {
                    "success": True,
                    "message": "Playlist renamed successfully!"
                }
            except mysql.connector.Error as err:
                print(f"Error renaming playlist: {err}")
                return {
                    "success": False,
                    "message": "Failed to rename playlist!"
                }
            
        else:
            return {
                "success": False,
                "message": "New playlist name is required for renaming playlist"
            }     

   