from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from .models import Location, ServiceRequest
from .serializers import LocationSerializer, ServiceRequestSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # filterset_fields = {'username': ['icontains'],
    #                     'last_name': ['icontains'],
    #                     'is_superuser': ['exact'],
    #                     'is_staff': ['exact'],
    #                     'is_active': ['exact'],
    #                     }


class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer