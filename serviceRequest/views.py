from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from .models import Location, ServiceRequest, RequestStatus, ServiceRequestChatMessage, MessageReading
from appUsers.models import CustomUser
from .serializers import LocationSerializer, ServiceRequestSerializer, RequestStatusSerializer, \
    ServiceRequestMessageSerializer, MessageReadingSerializer
from jose import jwt
from django.conf import settings
from rest_framework.decorators import action


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = {'location': ['icontains'],
                        }

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        payload = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
        user_data = CustomUser.objects.get(pk=payload['user_id'])
        if user_data.is_staff:
            return True
        else:
            return obj.request_sender == user_data


class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filterset_fields = {'request_sender': ['exact'], 'location': ['exact'], 'address': ['icontains'],
                        'request_status': ['exact'], 'executor': ['exact'], 'date_time_created': ['lte', 'gte'],
                        'executor': ['exact']
                        }

    @action(detail=True, methods=['get'])
    def get_unread_messages_count(self, request, pk=None):
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        payload = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
        user = CustomUser.objects.get(pk=payload['user_id'])
        service_request = self.get_object()
        all_messages = ServiceRequestChatMessage.objects.filter(service_request=service_request)
        read_messages = MessageReading.objects.filter(message__service_request=service_request, who_read=user)
        ids = [r.message.id for r in read_messages]
        serializer = ServiceRequestMessageSerializer(all_messages.exclude(id__in=ids), many=True)
        print('!!!!!!!!!!!', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # serializer = ServiceRequestMessageSerializer(data=)

        # service_request = self.get_object()
        # service_request_list = ServiceRequest.objects.all()
        # res = {}
        # for ser_req in service_request_list:
        #     full_count_of_messages = ser_req.servicerequestchatmessage_set.count()
        #     read_count = MessageReading.objects.filter(message__service_request=ser_req, who_read=user).count()
        #     res[ser_req.id] = full_count_of_messages - read_count
        # return Response(res, status=status.HTTP_200_OK)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestStatusViewSet(viewsets.ModelViewSet):
    queryset = RequestStatus.objects.all()
    serializer_class = RequestStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceRequestMessageViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequestChatMessage.objects.all()
    serializer_class = ServiceRequestMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = {'service_request': ['exact'], 'sender': ['exact'], 'message_text': ['icontains']}

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageReadingViewSet(viewsets.ModelViewSet):
    queryset = MessageReading.objects.all()
    serializer_class = MessageReadingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = {'message': ['exact'], 'who_read': ['exact']}

    def create(self, request, *args, **kwargs):
        serializer = MessageReadingSerializer(data=request.data)
        if serializer.is_valid():
            records_list = MessageReading.objects.filter(message_id=request.data['message'],
                                                         who_read_id=request.data['who_read'])
            if len(records_list) == 0:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_200_OK)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)
