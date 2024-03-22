import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack


from channels.security.websocket import AllowedHostsOriginValidator
# import sajiloroomfinder.routing  # Import websocket_urlpatterns from your app's routing module

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sajiloroomfinder.settings")

# Get the default Django ASGI application
django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_application,  # Route HTTP requests to Django application
    
})
