from rest_framework import serializers
from .models import Location, RequestStatus, ServiceRequest


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'location']


class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = ['id', 'status']


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['id', 'request_sender', 'location',
                  'address', 'request_description',
                  'request_status', 'executor', 'date_time_created', 'date_time_edited', 'get_request_status']