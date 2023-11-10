from django.db import models
from appUsers.models import CustomUser
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()
from asgiref.sync import async_to_sync


class Location(models.Model):
    location = models.TextField(verbose_name="Location")

    def __str__(self):
        return self.location

    class Meta:
        ordering = ('id',)
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


class RequestStatus(models.Model):
    status = models.CharField(max_length=100, verbose_name="Status")
    status_color = models.CharField(max_length=100, verbose_name="Status color", blank=True, null=True)

    def __str__(self):
        return self.status

    class Meta:
        ordering = ('id',)
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class ServiceRequest(models.Model):
    request_sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Request sender")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Location")
    address = models.TextField(verbose_name="Address")
    request_description = models.TextField(verbose_name="Description")
    request_status = models.ForeignKey(RequestStatus, on_delete=models.CASCADE, verbose_name="Status", default=1)
    executor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="executor", verbose_name="Executor",
                                 blank=True, null=True)
    date_time_created = models.DateTimeField(verbose_name="Date and time created", auto_now=True)
    date_time_edited = models.DateTimeField(verbose_name="Date and time edited", auto_now=True)

    def __str__(self):
        return self.request_sender.username + ' ' + self.request_description

    def save(self, *args, **kwargs):
        from .serializers import ServiceRequestSerializer
        super(ServiceRequest, self).save(*args, **kwargs)
        serializer = ServiceRequestSerializer(self)
        async_to_sync(channel_layer.group_send)(f"requests_{self.request_sender.id}",
                                                {"type": "chat.message", "message": serializer.data})

    @property
    def get_request_status_text(self):
        return self.request_status.status

    @property
    def get_request_status_color(self):
        return self.request_status.status_color

    @property
    def get_sender_name(self):
        return self.request_sender.username

    @property
    def get_executor_name(self):
        return self.executor.username

    @property
    def not_read_messages_count(self):
        return self.servicerequestchatmessage_set.filter(is_read=False).count()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'


class ServiceRequestChatMessage(models.Model):
    message_text = models.TextField(verbose_name="Message")
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, verbose_name="Service request")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Sender")
    is_read = models.BooleanField(verbose_name="Is read", default=False)

    def save(self, *args, **kwargs):
        from .serializers import ServiceRequestMessageSerializer, ServiceRequestSerializer
        super(ServiceRequestChatMessage, self).save(*args, **kwargs)
        serializer = ServiceRequestMessageSerializer(self)
        async_to_sync(channel_layer.group_send)(f"chat_{self.service_request.id}",
                                                {"type": "chat.message", "message": serializer.data})

        service_request_after_add_message = self.service_request
        serializer = ServiceRequestSerializer(service_request_after_add_message)
        async_to_sync(channel_layer.group_send)(f"requests_{self.service_request.request_sender.id}",
                                                {"type": "chat.message", "message": serializer.data})

    def __str__(self):
        return self.message_text

    class Meta:
        ordering = ('id',)
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
