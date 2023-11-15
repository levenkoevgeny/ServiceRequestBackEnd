from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status

from jose import jwt
import json
from django.conf import settings

from .models import CustomUser
from serviceRequest.models import ServiceRequest, ServiceRequestChatMessage, MessageReading
from .serializers import CustomUserSerializer, UserNamesSerializer, ChangePasswordSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = {'username': ['icontains'],
                        'last_name': ['icontains'],
                        'is_superuser': ['exact'],
                        'is_staff': ['exact'],
                        'is_active': ['exact'],
                        'can_be_executor': ['exact'],
                        }

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get_unread_messages_count_in_requests(self, request, pk=None):
        user = self.get_object()
        service_request_list = ServiceRequest.objects.all()
        res = {}
        for ser_req in service_request_list:
            full_count_of_messages = ser_req.servicerequestchatmessage_set.count()
            read_count = MessageReading.objects.filter(message__service_request=ser_req, who_read=user).count()
            res[ser_req.id] = full_count_of_messages - read_count
        return Response(res, status=status.HTTP_200_OK)






    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    try:
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        payload = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
    except jwt.JWTError:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user_data = CustomUser.objects.get(pk=payload['user_id'])
        serializer = CustomUserSerializer(user_data)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_registration(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        validated_data['is_active'] = True
        CustomUser.objects.create_user(**validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserNamesViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserNamesSerializer
    filterset_fields = {
        'username': ['exact'],
    }
