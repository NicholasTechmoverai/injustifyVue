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
        { label: "month", seconds: 2592000 },
        { label: "day", seconds: 86400 },
        { label: "hour", seconds: 3600 },
        { label: "minute", seconds: 60 },
    ];

    for (const interval of intervals) {
        const count = Math.floor(diffInSeconds / interval.seconds);
        if (count >= 1) {
            return `${count} ${interval.label}${count > 1 ? "s" : ""} ago`;
        }
    }

    return "just now";
}