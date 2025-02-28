from flask import Blueprint,Response,request,jsonify
from datetime import datetime
from config import Config
from typing import Optional, List, Dict, Union
import asyncio

from utils.yt_handler_YTDLP import download_stream
from utils.globalDb import insert_download

downloads_bp = Blueprint('downloads', __name__)

mydb = Config.mydb
mycursor = mydb.cursor()


@downloads_bp.route('<useremail>')
def get_downloads(useremail):
    print("getting downloads!! for",useremail)
    return jsonify({"downloads": fetch_downloads(useremail).get('downloads')})


def fetch_downloads(
    user_id: Optional[int] = None,
    song_id: Optional[str] = None,
    name: Optional[str] = None,
    date: Optional[Union[str, datetime]] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    order_by: Optional[str] = None
) -> Optional[List[Dict]]:
    """
    Fetch downloads from the database with flexible filtering, sorting, and pagination.
    
    Args:
        user_id (Optional[int]): User ID to filter downloads.
        song_id (Optional[str]): Song ID to filter downloads.
        name (Optional[str]): Name to filter downloads.
        date (Optional[Union[str, datetime]]): Date to filter downloads.
        limit (Optional[int]): Maximum number of records to return.
        offset (Optional[int]): Number of records to skip.
        order_by (Optional[str]): Column to sort the results.

    Returns:
        Optional[List[Dict]]: List of downloads or None in case of an error.
    """
    try:
        query = "SELECT * FROM downloads WHERE 1=1"
        values = []

        if user_id:
            if '@' in user_id and '.'  in user_id:
                qr=f"SELECT id FROM injustifyusers WHERE email = %s"
                mycursor.execute(qr, (user_id,))
                user_id = mycursor.fetchone()[0]                

            query += " AND user_id = %s"
            values.append(user_id)
        
        if song_id:
            query += " AND song_id = %s"
            values.append(song_id)
        
        if name:
            query += " AND filename LIKE %s"
            values.append(f"%{name}%")
        
        if date:
            query += " AND DATE(timestamp) = %s"
            values.append(date)
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit is not None:
            query += " LIMIT %s"
            values.append(limit)
        
        if offset is not None:
            query += " OFFSET %s"
            values.append(offset)

        mycursor.execute(query, values)
        results = mycursor.fetchall()

        downloads= [{
            'filesize': result[6],
            'filename': result[3],
            'thumbnail': result[14],
            'links': result[2],
            'timestamp': result[10].strftime('%Y-%m-%d %H:%M:%S'),
        } for result in results]
        return {
            "success": True,
            "downloads": downloads
        }

    except Exception as e:
        print(f"Error fetching downloads: {e}")
        return {
                    "success": False,
                    "downloads": []
                }



@downloads_bp.route('/download', methods=['POST'])
async def download_video():
    try:
        data = request.get_json() 
        url = data.get('url')
        itag = data.get('itag')
        filename = data.get('filename')
        start_byte = int(data.get('start_byte', 0))
        song_id = data.get('song_id')
        user_id = data.get('userId')
        file_size = data.get('file_size')
        thumbnail = data.get('thumbnailUrl')


        if not url or not itag or not filename :
            return jsonify({"error": "URL, itag, song ID, and filename are required"}), 400

        if user_id and song_id: 
            insert_download(
                user_id=user_id,
                song_id=song_id,
                file_name=filename,
                file_format= itag,
                itag = itag,
                file_size=file_size,
                file_source="youtube",
                thumbnail = thumbnail,
                user_agent=request.headers.get('User-Agent'),
                is_partial=(start_byte > 0),
            )

        content_type = "video/mp4"  # Adjust based on file format
        response = Response(
            download_stream(url, itag, start_byte),
            content_type=content_type,
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

