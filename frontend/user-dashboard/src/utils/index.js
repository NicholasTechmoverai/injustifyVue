export const BASE_URL = "http://127.0.0.1:5000";
export const AUTH_WITH_GOOGLE = `${BASE_URL}/login/google`
export const MANUAL_LOGIN = `${BASE_URL}/login`
export const SIGN_UP = `${BASE_URL}/signup`


export function timeAgo(time) {
    const now = new Date();

    const postTime = new Date(time);
    const diffInSeconds = Math.floor((now - postTime) / 1000);
    //console.log(now , postTime)
    const intervals = [
        { label: "year", seconds: 31536000 },
        { label: "mnth", seconds: 2592000 },
        { label: "d", seconds: 86400 },
        { label: "hr", seconds: 3600 },
        { label: "m", seconds: 60 },
    ];

    for (const interval of intervals) {
        const count = Math.floor(diffInSeconds / interval.seconds);
        if (count >= 1) {
            return `${count} ${interval.label}${count > 1 ? "s" : ""} ago`;
        }
    }

    return "just now";
}



export function getYouTubeThumbnails(url) {
    // Optimized regex to match YouTube video ID across all URL formats
    const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^/\n\s]+\/\S+\/|(?:v|e(?:mbed)?\/|.*[?&]v=))|youtu\.be\/|youtube\.com\/shorts\/)([^"&?/\s]{11})/;
    
    const match = url.match(regex);
    if (match && match[1]) {
        return `https://img.youtube.com/vi/${match[1]}/hqdefault.jpg`;
    }
    
    console.warn(`Invalid YouTube URL: ${url}`);
    return null;
}


let spotifyToken = null;
let tokenExpiration = 0; // Time when token expires

async function getSpotifyAccessToken() {
    const clientId = "ba5ea23c58884dcba54f767875aafcf1";     // Replace with your actual Client ID
    const clientSecret = "15f4c324944b47e88e41325efbce64c7"; // Replace with your actual Client Secret
    
    const credentials = `${clientId}:${clientSecret}`;
    const encodedCredentials = btoa(credentials);

    const response = await fetch("https://accounts.spotify.com/api/token", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": `Basic ${encodedCredentials}`,
        },
        body: "grant_type=client_credentials",
    });

    const data = await response.json();
    if (data.access_token) {
        spotifyToken = data.access_token;
        tokenExpiration = Date.now() + data.expires_in * 1000; 
        return spotifyToken;
    } else {
        console.error("Failed to fetch Spotify access token");
        return null;
    }
}

// Function to get a valid token (refreshes if expired)
async function getValidSpotifyToken() {
    if (!spotifyToken || Date.now() >= tokenExpiration) {
        console.log("Fetching new Spotify token...");
        return await getSpotifyAccessToken();
    }
    return spotifyToken;
}

// Function to get Spotify thumbnail
export async function getSpotifyThumbnail(songUrl) {
    const trackId = songUrl.split("track/")[1]?.split("?")[0]; // Extract track ID
    if (!trackId) {
        console.error("Invalid Spotify URL");
        return null;
    }

    const token = await getValidSpotifyToken(); 

    const response = await fetch(`https://api.spotify.com/v1/tracks/${trackId}`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();
    return data.album?.images[0]?.url || null; // Get the highest-quality image
}
