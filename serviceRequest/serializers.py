from rest_framework import serializers
from .models import Location, RequestStatus, ServiceRequest, ServiceRequestChatMessage


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
                  'get_request_status_color', 'get_sender_name', 'get_executor_name']


class ServiceRequestMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequestChatMessage
        fields = '__all__'
        depth = 1