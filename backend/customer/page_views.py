from django.shortcuts import get_object_or_404, render
from accounts.decorators import role_required
from categories.models import Category
from vendors.models import VendorProfile
from . models import CustomerProfile
from orders.models import Order,OrderItem


@role_required("customer")
def dashboard(request):
    vendors = VendorProfile.objects.all()
    context = {'vendors': vendors}
    return render(request, "customer/dashboard.html", context)


@role_required("customer")
def explore_vendor(request, slug):
    vendor = get_object_or_404(VendorProfile, slug=slug, is_active=True)
    products = vendor.products.filter(is_available=True)

    selected_category_slug = request.GET.get("category")
    if selected_category_slug:
        products = products.filter(category__slug=selected_category_slug)

    categories = Category.objects.filter(products__vendor=vendor, products__is_available=True).distinct()

    context = {
        'vendor': vendor,
        'products': products,
        'categories': categories,
        'selected_category_slug': selected_category_slug,
    }
    return render(request, "customer/dashboard.html", context)



@role_required('customer')
def order(request):
    customer = CustomerProfile.objects.filter(user = request.user)
    orders = Order.objects.filter(customer=request.user)
    for order in orders:
        # print(order.vendor.user.profile_picture.url)
        print("type is  ",type(order.vendor.user))
    context = {'customer':customer,"orders":orders}
    return render(request,'customer/dashboard.html',context)

