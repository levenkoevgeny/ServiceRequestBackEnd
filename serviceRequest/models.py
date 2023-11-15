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
    is_block_chat = models.BooleanField(verbose_name="Is blocking chat", default=False)

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
    def get_request_status_block(self):
        return self.request_status.is_block_chat

    @property
    def get_sender_name(self):
        return self.request_sender.username

    @property
    def get_executor_name(self):
        return self.executor.username

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'


class ServiceRequestChatMessage(models.Model):
    message_text = models.TextField(verbose_name="Message")
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, verbose_name="Service request")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Sender")
    date_time_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        from .serializers import ServiceRequestMessageSerializer
        super(ServiceRequestChatMessage, self).save(*args, **kwargs)
        serializer = ServiceRequestMessageSerializer(self)
        async_to_sync(channel_layer.group_send)(f"chat_{self.service_request.id}",
                                                {"type": "chat.message", "message": serializer.data})

        service_request_after_add_message = self.service_request
        admin_list = CustomUser.objects.filter(is_staff=True)
        for admin in admin_list:
            service_request_after_add_message.servicerequestchatmessage_set.count()
            unread_count = service_request_after_add_message.servicerequestchatmessage_set.count() - MessageReading.objects.filter(
                message__service_request=service_request_after_add_message,
                who_read=admin).count()
            async_to_sync(channel_layer.group_send)(f"unread_{admin.id}",
                                                    {"type": "chat.message",
                                                     "message": {str(service_request_after_add_message.id): unread_count}})
            unread_count_ = service_request_after_add_message.servicerequestchatmessage_set.count() - MessageReading.objects.filter(
                message__service_request=service_request_after_add_message,
                who_read=service_request_after_add_message.request_sender).count()
            async_to_sync(channel_layer.group_send)(f"unread_{service_request_after_add_message.request_sender.id}",
                                                    {"type": "chat.message",
                                                     "message": {str(service_request_after_add_message.id): unread_count_}})

    def __str__(self):
        return self.message_text

    class Meta:
        ordering = ('id',)
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class MessageReading(models.Model):
    message = models.ForeignKey(ServiceRequestChatMessage, on_delete=models.CASCADE, verbose_name="Message")
    who_read = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Who read")
    date_time_read = models.DateTimeField(auto_now_add=True, verbose_name="Date anf time of reading")

    def __str__(self):
        return str(self.message) + ' ' + str(self.who_read)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Message_Reading'
        verbose_name_plural = 'Message_Readings'
