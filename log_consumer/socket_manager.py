import socketio
import os

REDIS_HOST = os.getenv("REDIS_SOCKET_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

mgr = socketio.RedisManager(url=f"redis://{REDIS_HOST}:{REDIS_PORT}/0") 
sio: socketio.Server = socketio.Server(
    cors_allowed_origins="*", client_manager=mgr
)