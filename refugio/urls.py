from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from reservations.views import RoomViewSet, ClientViewSet, ReservationViewSet

router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
