from rest_framework import permissions, status, viewsets, mixins
from rest_framework.response import Response
from .models import Location, ServiceRequest
from .serializers import LocationSerializer, ServiceRequestSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = {'location': ['icontains'],
                        }

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    # permission_classes = [permissions.IsAdminUser]
    filterset_fields = {'request_sender': ['exact'], 'location': ['exact'], 'address': ['icontains'],
                        'request_status': ['exact'], 'executor': ['exact'], 'date_time_created': ['lte', 'gte']
                        }

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)