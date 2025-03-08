import { io } from "socket.io-client";

const socket = io("http://192.168.100.2:5000/inj-user", {
    path: "/ws/socket.io", // 🔥 Ensure correct WebSocket path
    transports: ["websocket"], // 🔥 Avoid long polling
    withCredentials: true, // 🔥 Send credentials if needed
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
