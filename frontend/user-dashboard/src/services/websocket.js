import { io } from "socket.io-client";
import {BASE_URL} from "@/utils/index.js";
import { useUserStore } from "@/store/index.js";

const socket = io(`${BASE_URL}/inj-user`, {
    path: "/ws/socket.io", 
    transports: ["websocket"], 
    withCredentials: true, 
});

    
socket.on("connect", () => {
    console.log("✅ Connected to WebSocket server");
    const userStore = useUserStore();
    userStore.set_snackbarMessage( 'Connected Back!','success',10000);
});

socket.on("disconnect", () => {
    console.log("❌ Disconnected from WebSocket server");
    const userStore = useUserStore();
    userStore.set_snackbarMessage('you\'r Offline !!','error',10000);
});

socket.on("message", (data) => {
    console.log("📩 Received:", data);
    const userStore = useUserStore();
    userStore.set_snackbarMessage(data.message,data.type,10000);


});

export default socket;



//Functions

export async function likeUnlikeSong(song_id,userId) {
    if (!userId && !song_id) {
      this.userStore.set_snackbarMessage("You need to login!!, ", "error", 10000);
      return;
    }
    socket.emit("likeUnlikeSong", { songId: song_id, userId: userId });
  }