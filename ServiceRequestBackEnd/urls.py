
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from appUsers import views as users_views
from serviceRequest import views as service_views
router = routers.DefaultRouter()

router.register(r'users', users_views.CustomUserViewSet)
router.register(r'locations', service_views.LocationViewSet)
router.register(r'service-requests', service_views.ServiceRequestViewSet)
router.register(r'usernames', users_views.UserNamesViewSet)
router.register(r'statuses', service_views.RequestStatusViewSet)
router.register(r'messages', service_views.ServiceRequestMessageViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='/api')),
    path('api/users/me/', users_views.get_me),
    path('api/users/user-registration/', users_views.user_registration),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
