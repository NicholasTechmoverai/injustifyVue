from pytube import Search,YouTube
import json
import os


import requests
import logging
from pytube import Search

logging.basicConfig(level=logging.INFO)

api_key = os.getenv('YOUTUBE_API_KEY')


def search_videos_pytube(query):
    """Fetch YouTube search results using PyTube as a fallback."""
    try:
        logging.info("Using PyTube as fallback for YouTube search...")
        search = Search(query)

        # Ensure search.results is populated
        if not search.results:
            logging.warning("No results found using PyTube.")
            return []

        return [
            {"title": video.title, "url": video.watch_url}
            for video in search.results
        ]
    except Exception as e:
        logging.error(f"Error in search_videos_pytube: {str(e)}")
        return []


def search_videos_yt(search_query):
    """Fetch YouTube search results using the API, fallback to PyTube on failure."""
    url = "https://www.googleapis.com/youtube/v3/search"

    #print(f"Searching YouTube for: {search_query}")

    params = {
        "part": "snippet",
        "q": search_query,
        "type": "video",
        "maxResults": 20,
        "key": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)

        data = response.json()

        if "items" not in data:
            logging.warning("Invalid API response, falling back to PyTube.")
            return search_videos_pytube(search_query)

        return [
            {
                "title": video["snippet"]["title"],
                "url": f'https://www.youtube.com/watch?v={video["id"]["videoId"]}',
            }
            for video in data.get("items", []) if "videoId" in video.get("id", {})
        ]

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {str(e)}. Falling back to PyTube...")
        return search_videos_pytube(search_query)




from googleapiclient.discovery import build

from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build

def get_video_id(video_url):
    """Extracts video ID from a YouTube URL."""
    parsed_url = urlparse(video_url)
    if parsed_url.hostname == "youtu.be":  # Shortened URL
        return parsed_url.path[1:]  # Remove the leading "/"
    elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:  # Standard URL
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]
    else:
        return None

def get_youtube_video_details(video_url):
    print('invoked and working!!',video_url)
    """Fetches YouTube video details using the YouTube Data API."""
    # Your API key from Google Cloud Console

    # Extract video ID
    video_id = get_video_id(video_url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}

    # Build the YouTube API client
    youtube = build("youtube", "v3", developerKey=api_key)

    # Call the API to get video details
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    #print(response)

    # Extract relevant details
    if response["items"]:
        video_details = response["items"][0]
        
        # Extracting details from the response
        title = video_details["snippet"]["title"]
        views = video_details["statistics"]["viewCount"]
        duration = video_details["contentDetails"]["duration"]
        likes = video_details["statistics"].get("likeCount")  # Only if provided
        dislikes = "Not available"  # YouTube no longer provides dislikeCount publicly

        return{
            "success":True,
            "info":{
                "title": title,
                "views": views,
                "duration": duration,
                "likes": likes if likes else "Not available",
                "dislikes": dislikes,
                }
        }

    else:
        return {"error": "Video not found or invalid URL"}

# Example usage


#print(search_videos_yt('enya only time'))
