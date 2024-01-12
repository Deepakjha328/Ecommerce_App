from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from product.models import Product
from authorization.models import Address

User = get_user_model()


class Order(models.Model):
    PENDING = "P"
    COMPLETED = "C"

    STATUS_CHOICES = ((PENDING, _("pending")), (COMPLETED, _("completed")))

    buyer = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    shipping_address = models.ForeignKey(Address, related_name="shipping_orders", on_delete=models.SET_NULL,blank=True, null=True,)
    billing_address = models.ForeignKey(Address, related_name="billing_orders", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.buyer.get_full_name()

    @cached_property
    def total_cost(self):
        """
        Total cost of all the items in an order using aggregate function.
        """
        total = self.order_items.aggregate(
            total_cost=Sum(F('product__price')*F('quantity'))
        )['total_cost']
        return round(total, 2) if total is not None else 0


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product_orders", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.order.buyer.get_full_name()

    @cached_property
    def cost(self):
        """
        Total cost of the ordered item
        """
        return round(self.quantity * self.product.price, 2)