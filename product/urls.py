from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ScriptView, ProductCategoryViewset

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'product_category', ProductCategoryViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('script/', ScriptView.as_view()),
]