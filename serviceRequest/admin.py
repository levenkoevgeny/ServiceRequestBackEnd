from django.contrib import admin
from .models import RequestStatus, ServiceRequestChatMessage


admin.site.register(RequestStatus)
admin.site.register(ServiceRequestChatMessage)
