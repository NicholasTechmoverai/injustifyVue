import { io } from "socket.io-client";
import {BASE_URL} from "@/utils/index.js";

const socket = io(`${BASE_URL}/inj-user`, {
    path: "/ws/socket.io", 
    transports: ["websocket"], 
    withCredentials: true, 
});

    
socket.on("connect", () => {
    console.log("✅ Connected to WebSocket server");
});

socket.on("disconnect", () => {
    console.log("❌ Disconnected from WebSocket server");
});

socket.on("message", (data) => {
    console.log("📩 Received:", data);
});

export default socket;
