from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save,m2m_changed

# Create your models here.

User = settings.AUTH_USER_MODEL

from products.models import Product


class CartManager(models.Manager):
    def new_or_get(self,request):
        cart_id = request.session.get("card_id,None")
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count()==1:
            new_object = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            new_object = True
            cart_obj = cart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj,new_object


    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class cart(models.Model):
    user            = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    products        = models.ManyToManyField(Product,blank=True)
    total           = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def pre_save_cart_receiver(sender,instance,*args,**kwargs):
    products = instance.products.all()
    total = 0
    for x in products:
        total += x.price
    print(total)
    instance.total = total

m2m_changed.connect(pre_save_cart_receiver,sender=cart.products.through)



