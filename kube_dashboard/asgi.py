import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from authentication.session import KubeSessionMiddlewareStack
from kube_resource.urls import websocket_urlpatterns as resource_ws_urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kube_dashboard.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": KubeSessionMiddlewareStack(
        URLRouter(
            resource_ws_urls
        )
    ),
})
