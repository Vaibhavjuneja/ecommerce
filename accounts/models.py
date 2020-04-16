from django.db import models

class GuestEmail(models.Model):
    email = models.EmailField()
    updated     = models.DateTimeField(auto_now=True)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


