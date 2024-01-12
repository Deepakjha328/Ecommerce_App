from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from . models import Order, OrderItem
from rest_framework import viewsets, status
from product.models import Product
from . serializers import (OrderItemSerializer, OrderSerializer)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


    def get_queryset(self):
        if self.query_params.get('id'):
            return self.queryset.filter(id=self.query_params.get('id'))
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):
        """ Custom delete behavior, if necessary """
        order_item = self.get_object()
        order_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        """ Custom update behavior, if necessary """
        partial = kwargs.pop('partial', False)
        order_item = self.get_object()
        serializer = self.get_serializer(order_item, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_superuser:
            return self.queryset.filter(buyer=user)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        user = self.request.user  # Assuming you're using Django's authentication
        print(user)
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        product = Product.objects.get(id=product_id)

        
        # Fetch or create the order for the user
        order, created_order = Order.objects.get_or_create(buyer=user, status="pending", defaults={'buyer': user})

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST)

        order_item, created_item = OrderItem.objects.get_or_create(order=order, product=product)

        if order_item.quantity > product.quantity:
            error = {"quantity": ("Ordered quantity is more than the stock.")}
            raise ValidationError(error)

        # if self.request.user == product.seller:
        #     error = ("Adding your own product to your order is not allowed")
        #     raise PermissionDenied(error)

        # if not created_item:
        #     # Update quantity if the item already exists
        #     order_item.quantity += int(quantity)
        # else:
        if quantity==0:
            order_item.delete()
        order_item.quantity = int(quantity)
        order_item.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created_item else status.HTTP_200_OK)
    