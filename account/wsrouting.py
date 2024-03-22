from django.urls import re_path
from . import wsconsumers

websocket_urlpatterns=[
    re_path(r'ws/test/', wsconsumers.SyncTestConsumer.as_asgi())
]