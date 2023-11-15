from rest_framework import serializers
from .models import Location, RequestStatus, ServiceRequest, ServiceRequestChatMessage, MessageReading
from appUsers.serializers import CustomUserSerializer


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'location']


class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = ['id', 'status', 'status_color']


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['id', 'request_sender', 'location',
                  'address', 'request_description',
                  'request_status', 'executor', 'date_time_created', 'date_time_edited', 'get_request_status_text',
                  'get_request_status_color', 'get_sender_name', 'get_executor_name',
                  'get_request_status_block']


class ServiceRequestMessageSerializer(serializers.ModelSerializer):
    service_data = ServiceRequestSerializer(read_only=True, source='service_request')
    sender_data = CustomUserSerializer(read_only=True, source='sender')

    class Meta:
        model = ServiceRequestChatMessage
        fields = ['id', 'message_text', 'service_request', 'sender', 'service_data', 'sender_data',
                  'date_time_created']


class MessageReadingSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageReading
        fields = '__all__'