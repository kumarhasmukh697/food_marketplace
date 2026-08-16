from django.shortcuts import render
from accounts.decorators import role_required
from products.models import Product

@role_required("vendor")
def dashboard(request):
    return render(request,'vendor/v-dashboard.html')



@role_required("vendor")
def orders(request):
    return render(request,'vendor/v-dashboard.html')


@role_required("vendor")
def menu(request):
    vendor_profile = request.user.vendor_profile
    products = Product.objects.filter(vendor=vendor_profile)
    context = {
        'products': products
    }
    return render(request,'vendor/v-dashboard.html',context)