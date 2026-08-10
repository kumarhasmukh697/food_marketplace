from django.shortcuts import render
from products.models import Product
from vendors.models import VendorProfile

def home(request):
    # Fetch all products and vendors
    vendors = VendorProfile.objects.all()
    context = {'vendors': vendors}
    for vendor in vendors:
        print(vendor.shop_name)
    return render(request,'home.html',context)

# register view
def register(request):
    return render(request,'accounts/register.html')

# login view
def login(request):
    return render(request,'accounts/login.html')

# verifyotp view
def verifyotp(request):
    return render(request,'accounts/verify-otp.html')

