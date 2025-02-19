const WebSocketService = {
    socket: null,
  
    connect() {
      this.socket = new WebSocket('w//127.0.0.1:5000/ws'); // Replace with actual WebSocket URL
  
      this.socket.onopen = () => {
        console.log('WebSocket connected');
      };
  
      this.socket.onmessage = (event) => {
        console.log('Received:', event.data);
      };
  
      this.socket.onerror = (error) => {
        console.error('WebSocket Error:', error);
      };
  
      this.socket.onclose = () => {
        console.log('WebSocket disconnected');
      };
    },
  
    sendMessage(message) {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify(message));
      }
    }
  };
  
  export default WebSocketService;
  