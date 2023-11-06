from django.db import models
from appUsers.models import CustomUser


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

    @property
    def get_request_status(self):
        return self.request_status.status

    class Meta:
        ordering = ('id',)
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'