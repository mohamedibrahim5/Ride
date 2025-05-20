import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
http_application = get_asgi_application()


async def lifespan_application(scope, receive, send):
    if scope["type"] == "lifespan":
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return


application = ProtocolTypeRouter(
    {
        "http": http_application,
        "lifespan": lifespan_application,
    }
)
