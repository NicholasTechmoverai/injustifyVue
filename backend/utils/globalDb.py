import logging
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
    