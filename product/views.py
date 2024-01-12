from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from . serializers import ProductCategorySerializer, ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category","name",)

    def get_queryset(self):
        if self.request.query_params.get('id'):
            return self.queryset.filter(id=self.request.query_params.get('id'))
        return super().get_queryset()


class ProductCategoryViewset(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("name",)

class ScriptView(APIView):
    def get(self, request):
        product_list = ["Mobile", "Laptop", "Tablet", "Desktop", "Microphone"]
        for product in product_list:
            ProductCategory.objects.create(name=product)
        return Response("Updated")