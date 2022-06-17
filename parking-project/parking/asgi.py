# mysite/asgi.py
import os
import django

from .channelsmiddleware import TokenAuthMiddlewareStack
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking.settings')

django.setup()


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": TokenAuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
