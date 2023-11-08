import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from serviceRequest.models import ServiceRequestChatMessage
from serviceRequest.serializers import ServiceRequestMessageSerializer


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

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        new_message = ServiceRequestChatMessage.objects.create(message_text=text_data_json["message"],
                                                 sender_id=text_data_json["sender"],
                                                 service_request_id=text_data_json["service_request"])

        serializer = ServiceRequestMessageSerializer(new_message)

        # # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": serializer.data}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))
