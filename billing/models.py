from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from accounts.models import Guest
User = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        obj = None
        created = False

         # Logged in user checkout. Remembers payment
        if user.is_authenticated:
            obj,created = self.model.objects.get_or_create(user=user, email=user.email)
            # Guest user checkout. autoreloads payment
        elif guest_email_id is not None:
            guest_obj = Guest
            guest_email_obj = guest_obj.objects.get(id=guest_email_id)
            obj,created = self.model.objects.get_or_create(email=guest_email_obj.email)
            created = True
        else:
            created = False
        return obj, created

class BillingProfile(models.Model):
    user = models.OneToOneField(User, unique=True, null=True, blank=True, on_delete=models.DO_NOTHING)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateField(auto_now=True)
    timestamp = models.DateField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

# def billing_profile_created_reciever(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.customer_id = new_id
#         instance.save()

def user_created_reciever(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)
post_save.connect(user_created_reciever, sender=User)
