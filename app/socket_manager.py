import socketio
import os

REDIS_HOST = os.getenv("REDIS_SOCKET_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

mgr = socketio.AsyncRedisManager(url=f"redis://{REDIS_HOST}:{REDIS_PORT}/0") 
sio: socketio.AsyncServer = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="*", client_manager=mgr
)