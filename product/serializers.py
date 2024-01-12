from rest_framework import serializers
from orders.models import OrderItem
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    qty = serializers.SerializerMethodField()
    def get_qty(self, instance):
        qty =  OrderItem.objects.filter(order__buyer=self.context.get('request').user, product=instance)
        if qty:
            return qty.first().quantity
        else:
            return 0
    
    class Meta:
        model = Product
        fields = ('id', 'seller', 'category', 'name', 'desc', 'image_url', 'price', 
                  'quantity', 'created_at', 'updated_at', 'qty')
        

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'icon_image', 'created_at', 'updated_at']