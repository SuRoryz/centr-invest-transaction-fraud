import socketio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from socket_manager import sio
from routers.routers import router
from routers.view import router as views

class NoPrefixNamespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        print("connect ", sid)

    def on_disconnect(self, sid):
        print("disconnect ", sid)

app = FastAPI()

sio.register_namespace(NoPrefixNamespace("/"))
sio_asgi_app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app)

app.mount("/static", StaticFiles(directory="./build/static"), name="static")

app.add_route("/socket.io/", route=sio_asgi_app, methods=["GET", "POST"])
app.add_websocket_route("/socket.io/", sio_asgi_app)

app.include_router(router)
app.include_router(views)


@sio.on('subscribe_logs')
async def subscribe_logs(sid):
    await sio.enter_room(sid, "listen_log")