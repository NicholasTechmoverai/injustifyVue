import os
import re
from flask import Flask, request, jsonify, send_file,Blueprint,Response
from config import Config
import logging

song_folder = Config.SONGS_FOLDER


stream_bp = Blueprint('stream_local', __name__)


@stream_bp.route('/<filename>')
def stream_video(filename):
    file_name = filename
    logging.error(f"Requested file: {file_name}")

    if not file_name:
        logging.error("File parameter is missing")
        return Response("File parameter is required", status=400)

    # Secure the filename and ensure safe file paths
    #file_name = secure_filename(file_name)


    file_path = os.path.join(song_folder, file_name)
    logging.info(f"Streaming file🛬🛬: {file_path}")

    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return Response("File not found", status=404)

    file_size = os.path.getsize(file_path)

    chunk_size = calculate_chunk_size(file_size)

    # Handling Range requests
    range_header = request.headers.get('Range', None)
    if range_header:
        try:
            range_match = re.search(r"bytes=(\d+)-(\d*)", range_header)
            if not range_match:
                return Response("Invalid Range header", status=416)
            start = int(range_match.group(1))
            end = int(range_match.group(2)) if range_match.group(2) else file_size - 1

            # Ensure valid range
            if start >= file_size or end >= file_size:
                return Response("Requested range not satisfiable", status=416)

            # Stream the requested chunk
            with open(file_path, 'rb') as f:
                f.seek(start)
                chunk = f.read(end - start + 1)

            response = Response(chunk, status=206, mimetype='video/mp4')
            response.headers['Content-Range'] = f"bytes {start}-{end}/{file_size}"
            response.headers['Accept-Ranges'] = 'bytes'
            response.headers['Content-Length'] = len(chunk)
            return response

        except ValueError:
            return Response("Invalid Range header", status=400)
    
    # If no range is requested, return the whole file in dynamic chunks
    with open(file_path, 'rb') as f:
        chunk = f.read()

    response = Response(chunk, mimetype='video/mp4')
    response.headers['Content-Length'] = len(chunk)
    return response


def calculate_chunk_size(file_size):
    """
    Dynamically calculates chunk size based only on the file size.
    Small files (< 5MB) get smaller chunks for better handling.
    
    :param file_size: The size of the file in bytes.
    :return: Calculated chunk size in bytes.
    """
    # Special case: Files smaller than 5MB will have a fixed chunk size of 450 KB
    if file_size < 5 * 1024 * 1024:  # Less than 5MB
        return 450 * 1024  # 450 KB chunk size
    
    # For files 5MB and larger, use a dynamic chunk size based on file size
    elif file_size < 50 * 1024 * 1024:  # Between 5MB and 50MB
        return 1 * 1024 * 1024  # 1 MB chunk for medium-sized files
    
    elif file_size < 200 * 1024 * 1024:  # Between 50MB and 200MB
        return 2 * 1024 * 1024  # 2 MB chunk for larger files
    
    else:  # Files larger than 200 MB
        return 5 * 1024 * 1024  # 5 MB chunk for very large files
    
    

"""from flask import send_from_directory

@stream_bp.route('/<filename>')
def stream_video(filename):
    file_name = filename
    file_path = os.path.join(song_folder, file_name)

    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return Response("File not found", status=404)

    logging.info(f"Streaming file🛬🛬: {file_path}")

    return send_from_directory(song_folder, file_name, mimetype="video/mp4")
"""