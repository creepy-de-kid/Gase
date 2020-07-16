from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPES = (('billing', 'billing'),('shipping', 'shipping'))

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    country = models.CharField(max_length=120, default='Nigeria')
    state = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=120)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line1 = models.CharField(max_length=120)
    address_line2 = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return str(self.billing_profile)
