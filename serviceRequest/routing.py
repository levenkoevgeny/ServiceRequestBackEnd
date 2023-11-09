from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<service_request_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/requests/(?P<user_id>\w+)/$", consumers.ServiceRequestsConsumer.as_asgi()),
]