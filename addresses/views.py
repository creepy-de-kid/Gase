from django.shortcuts import render, redirect
from .forms import AddressForm
from billing.models import BillingProfile
from django.utils.http import is_safe_url

def checkout_address_create(request):
    form = AddressForm(request.POST or None)
    context = {
        'form':form
    }

    next_post = request.POST.get('next')
    redirect_path = next_post

    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile = BillingProfile.objects.new_or_get(request)[0]
        address_type = request.POST.get('address_type', 'shipping')

        if billing_profile != None:
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()

            request.session[address_type + "_address_id"] = instance.id
            billing_address_id = request.session.get('billing_address_id')
            shipping_address_id = request.session.get('shipping_address_id')
        else:
            print('Error: NO billing profile')
            return redirect('cart:checkout')

        safe_redirect = is_safe_url(redirect_path, request.get_host())
        print(safe_redirect)
        if safe_redirect:
            return redirect(redirect_path)
        else:
            return redirect('cart:checkout')

    return redirect('cart:checkout')