from flask import Blueprint,Response,request,jsonify
from datetime import datetime
from config import Config
import asyncio

from utils.yt_handler_YTDLP import download_stream
from utils.globalDb import insert_download

downloads_bp = Blueprint('downloads', __name__)

mydb = Config.mydb
mycursor = mydb.cursor()





from flask import Blueprint, request, jsonify, Response
import requests
import yt_dlp
import mimetypes

downloads_bp = Blueprint('downloads', __name__)

@downloads_bp.route('/download/yt', methods=['POST'])
async def download_video():
    print("Processing download request...")

    try:
        # Parse request data
        data = request.get_json()
        url = data.get('songId')
        itag = data.get('itag')
        filename = data.get('filename')
        start_byte = int(data.get('start_byte', 0))
        user_id = data.get('userId')
        file_size = data.get('file_size')
        thumbnail = data.get('thumbnailUrl')

        # Validate required fields
        if not url or not itag or not filename:
            return jsonify({"error": "songId, itag, and filename are required"}), 400

        # Insert download record if user_id is provided
        if user_id:
            insert_download(
                user_id=user_id,
                song_id=url,  # Using songId as song identifier
                file_name=filename,
                file_format=itag,
                itag=itag,
                file_size=file_size,
                file_source="youtube",
                thumbnail=thumbnail,
                user_agent=request.headers.get('User-Agent'),
                is_partial=(start_byte > 0),
            )

        # Dynamically determine content type
        content_type, _ = mimetypes.guess_type(filename)
        if not content_type:
            content_type = "video/mp4"  # Default to MP4 if unknown

        # Return response with stream generator
        response = Response(
            download_stream(url, itag, start_byte),
            content_type=content_type,
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Accept-Ranges': 'bytes',  # Support resuming downloads
            }
        )
        return response

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

