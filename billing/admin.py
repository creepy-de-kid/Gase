from django.contrib import admin
from .models import BillingProfile

class BillingAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'active', 'timestamp')
    list_display_links = ('user', 'email')

admin.site.register(BillingProfile, BillingAdmin)
