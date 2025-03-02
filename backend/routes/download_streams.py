import math,os
import threading
import os
from ffmpeg import probe
import mimetypes
from config import Config
from flask import Blueprint,request,jsonify
from utils.yt_handler_YTDLP import get_streams
import asyncio


download_folder = Config.SONGS_FOLDER
d_streams_bp = Blueprint('download_streams', __name__)


@d_streams_bp.route('/injustify/<filename>', methods=['GET'])
def get_streams_local(filename):
    if filename:
        file_path = os.path.join(download_folder, filename)

        # Check if the file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "message": "File not found in storage."
            }

        # Get file size in MB
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

        # Get MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        filename_without_extension = '.'.join(filename.split('.')[:-1])
        metadata = {
            "title": filename_without_extension,
            #"path": file_path,
            "type": mime_type or "unknown",
            "size_mb": file_size_mb,
            "success": True,
            'info': {
                "title": filename_without_extension,
                "artist": filename,
                "description": "",
                "views": ""
            }
        }
        # If the file is a video or audio, fetch additional details using ffprobe
        if mime_type and ("video" in mime_type or "audio" in mime_type):
            try:
                media_info = probe(file_path)
                # Extract streams info
                streams = media_info.get("streams", [])
                video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
                audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

                if video_stream:
                    metadata.update({
                        "resolution": f"{video_stream.get('width', 0)}x{video_stream.get('height', 0)}",
                        "video_codec": video_stream.get("codec_name", "unknown"),
                        "width": int(video_stream.get("width", 0)),
                        "height": int(video_stream.get("height", 0)),
                        "vbr": math.ceil(int(video_stream.get("bit_rate", 0)) / 1000) if video_stream.get("bit_rate") else 0,  # in kbps
                    })

                if audio_stream:
                    metadata.update({
                        "audio_codec": audio_stream.get("codec_name", "unknown"),
                        "abr": math.ceil(int(audio_stream.get("bit_rate", 0)) / 1000) if audio_stream.get("bit_rate") else 0,  # in kbps
                    })

                # Add duration (in seconds)
                duration = float(media_info.get("format", {}).get("duration", 0))
                metadata["duration"] = round(duration, 2)  # in seconds

            except Exception as e:
                metadata.update({
                    "error": f"Failed to extract media info: {str(e)}"
                })

        # Return the metadata wrapped in a list with three duplicates
        return [metadata] * 3
    else:
        return {
            "success": False,
            "message": "Filename is required to fetch streams."
        }





@d_streams_bp.route('/youtube', methods=['POST'])
def getStreams():
    try:
        data = request.json  # If JSON is sent
        if not data:
            data = request.form  # Check form-data as fallback

        link = data.get('songId')

        print("Getting streams for:", link)

        if not link:
            return jsonify({
                'success': False,
                'message': 'No link provided. Please provide a valid YouTube link.',
                'msg_type': "ERROR"
            }), 400

        # Fetch streams using the helper function
        streams = get_streams(link) 
        #print("Streams fetched successfully.",streams)  # Debugging log

        if streams.get('success'):
            return jsonify({
                'success': True,
                'streams': streams.get('streams'),
                'info': streams.get('info'),
                'link': link,
                'msg': streams.get('help_msg'),
                'msg_type': streams.get('msg_type', "HELP"),
            }), 200

        # If streams fetching failed
        return jsonify({
            'success': False,
            'message': streams.get('message', 'Unable to fetch streams.'),
            'msg_type': "ERROR"
        }), 500

    except Exception as e:
        print(f"Error in /streams endpoint: {str(e)}")  # Debugging log

        return jsonify({
            'success': False,
            'message': f"An unexpected error occurred: {str(e)}",
            'msg_type': "ERROR"
        }), 500
