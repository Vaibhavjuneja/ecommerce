from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

class BillingProfile(models.Model):
    user        = models.OneToOneField(User,unique=True,null=True,blank=True,on_delete=models.CASCADE)
    email       = models.EmailField()
    updated     = models.DateTimeField(auto_now=True)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email



# def billing_profile_created_receiver(sender,instance,created,*args,**kwargs):
#     if created:
#         print("send to stripe/braintree")
#         instance.customer_id = newID
#         instance.save()

def user_created_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)


post_save.connect(user_created_receiver,sender=User)
