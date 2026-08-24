from django.shortcuts import render
from accounts.decorators import role_required
from .models import VendorProfile
from products.models import Product
from orders.models import Order, OrderItem



@role_required("vendor")
def dashboard(request):
    return render(request,'vendor/v-dashboard.html')




@role_required("vendor")
def orders(request):
    user = request.user
    vendor = user.vendor_profile
    orders = vendor.orders.all()
    order_items = OrderItem.objects.filter()
    context = {"orders":orders}
    return render(request,'vendor/v-dashboard.html',context)


@role_required("vendor")
def menu(request):
    vendor_profile = request.user.vendor_profile
    products = Product.objects.filter(vendor=vendor_profile)
    context = {
        'products': products
    }
    return render(request,'vendor/v-dashboard.html',context)