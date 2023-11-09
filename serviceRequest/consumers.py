import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["service_request_id"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))


class ServiceRequestsConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["url_route"]["kwargs"]["user_id"]
        self.user_group_name = f"requests_{self.user}"

        async_to_sync(self.channel_layer.group_add)(
            self.user_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.user_group_name, self.channel_name
        )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))