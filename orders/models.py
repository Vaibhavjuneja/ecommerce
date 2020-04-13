from django.db import models

from carts.models import cart

ORDER_STATUS_CHOICES = (
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),
)

class Order(models.Model):
    cart         = models.ForeignKey(cart,on_delete=models.CASCADE)
    status        = models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    order_id            = models.CharField(max_length=120,blank=True)
    shipping_total      = models.DecimalField(default=5.90,max_digits=100,decimal_places=2)
    total            = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)


    def __str__(selfself):
        return self.order_id

