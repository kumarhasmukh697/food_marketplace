from django.shortcuts import render
from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
from accounts.decorators import role_required
from .models import VendorProfile
from products.models import Product
from orders.models import Order, OrderItem
from .utils import generate_sales_chart



@role_required("vendor")
def dashboard(request):
    vendor = VendorProfile.objects.get(user=request.user)
    products = Product.objects.filter(vendor=vendor,is_available=True)
    orders = vendor.orders.all()
    today_orders = Order.objects.filter(created_at__date=timezone.now().date())
    # Calculate total sum of today's orders
    today_sum = today_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    # Get yesterday's date
    yesterday = timezone.now().date() - timedelta(days=1)
    yesterday_orders = Order.objects.filter(created_at__date=yesterday)
    yesterday_sum = yesterday_orders.aggregate(total=Sum('total_amount'))['total'] or 0


    # 2. Calculate percentage change safely
    if yesterday_sum > 0:
        percent_change = ((today_sum - yesterday_sum) / yesterday_sum) * 100
    elif today_sum > 0:
        percent_change = 100.0  # 100% growth if yesterday was 0 and today has sales
    else:
        percent_change = 0.0    # 0% change if both days are 0
   
    context = {
        "products":products,
        "orders":orders,
        "today_orders":today_orders,
        "today_sum":today_sum,
        "percent_change":percent_change,
        }
    return render(request,'vendor/v-dashboard.html',context)




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



@role_required("vendor")
def analytics(request):
    vendor = VendorProfile.objects.get(user=request.user)
    total_order = vendor.orders.all()
    revenue = total_order.aggregate(total=Sum('total_amount'))['total'] or 0


    sales_chart = generate_sales_chart(vendor)
   

    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=7)

    # Fetch all orders created in the last 7 days (including today)
    last_7_days_orders = vendor.orders.filter(created_at__date__gte=seven_days_ago)

    # average order sum
    avg_order_sum = 0
    for order in total_order:
        avg_order_sum = avg_order_sum + order.subtotal
    avg_order_sum = avg_order_sum//(len(total_order))
    
    context={
        "vendor":vendor,
        "total_order":total_order,
        "avg_order_sum":avg_order_sum,
        "revenue":revenue,
        "last_7_days_orders":last_7_days_orders,
        "sales_chart": sales_chart,
    }
    return render(request,'vendor/v-dashboard.html',context)








