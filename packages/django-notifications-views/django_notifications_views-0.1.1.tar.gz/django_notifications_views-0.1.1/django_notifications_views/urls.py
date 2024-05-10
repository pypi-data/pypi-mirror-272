from rest_framework.routers import DefaultRouter
from django_notifications_views.views import NotificationsViewSet, ManageDeviceExpo


router = DefaultRouter()
router.register(r"user-notifications", NotificationsViewSet, basename="notifications")
router.register(r"expo-devices", ManageDeviceExpo, basename="expo")


# fmt: off
urlpatterns = [

]
# fmt: on