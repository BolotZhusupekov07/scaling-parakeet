from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from carts.models import CartCheckout


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=CASCADE)
    cart = models.ForeignKey(CartCheckout, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_order_price = models.DecimalField(max_digits=50,
                                            decimal_places=2)
    total_order_price_with_discount = models.DecimalField(max_digits=50,
                                            decimal_places=2, default=0)
