from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . views import OrderItemViewSet

# app_name = "order"

router = DefaultRouter()
# router.register(r"^(?P<order_id>\d+)/order-items", OrderItemViewSet)
router.register(r"order_item", OrderItemViewSet)


urlpatterns = [
    path("", include(router.urls)),
]