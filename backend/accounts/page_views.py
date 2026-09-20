from django.shortcuts import render
from django.conf import settings
from products.models import Product
from vendors.models import VendorProfile

def home(request):
    # Fetch all products and vendors
    print("hii user is :",request.user)
    vendors = VendorProfile.objects.all()
    context = {
        'vendors': vendors,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
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

