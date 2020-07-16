from django.db import models

class Guest(models.Model):
    email = models.EmailField(max_length=100)
    active = models.BooleanField(default=True)
    update = models.DateField(auto_now=True)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email
