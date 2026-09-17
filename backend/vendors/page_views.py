from django.shortcuts import render
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
from django.db.models import F, Sum
from django.utils import timezone
from accounts.decorators import role_required
from .models import VendorProfile
from products.models import Product
from orders.models import Order, OrderItem
from .utils import generate_sales_chart

SALES_STATUSES = [
    "confirmed",
    "preparing",
    "ready",
    "picked_up",
    "out_for_delivery",
    "delivered",
]



@role_required("vendor")
def dashboard(request):
    vendor = VendorProfile.objects.get(user=request.user)
    products = Product.objects.filter(vendor=vendor,is_available=True)
    today_orders = vendor.orders.filter(status='confirmed',created_at__date=timezone.now().date())
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
        "percent_change":round(percent_change,2)
        }
    return render(request,'vendor/v-dashboard.html',context)




@role_required("vendor")
def orders(request):
    vendor = VendorProfile.objects.get(user=request.user)
    orders = vendor.orders.all()
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
    today = timezone.localdate()
    current_month_start = today.replace(day=1)
    previous_month_end = current_month_start - timedelta(days=1)
    previous_month_start = previous_month_end.replace(day=1)

    sales_orders = vendor.orders.filter(status__in=SALES_STATUSES)
    total_order = sales_orders
    revenue = sales_orders.filter(
        created_at__date__gte=current_month_start,
        created_at__date__lt=today + timedelta(days=1),
    ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")
    previous_month_revenue = sales_orders.filter(
        created_at__date__gte=previous_month_start,
        created_at__date__lt=current_month_start,
    ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")

    if previous_month_revenue:
        revenue_change = round(
            float((revenue - previous_month_revenue) / previous_month_revenue * 100),
            1,
        )
    elif revenue:
        revenue_change = 100.0
    else:
        revenue_change = 0.0

    top_selling_items = (
        OrderItem.objects.filter(
            order__vendor=vendor,
            order__status__in=SALES_STATUSES,
        )
        .values("product_id", "product_name")
        .annotate(
            units_sold=Sum("quantity"),
            item_revenue=Sum("subtotal"),
            product_image=F("product__image"),
        )
        .order_by("-units_sold", "-item_revenue")[:3]
    )


    sales_chart = generate_sales_chart(vendor)
    seven_days_ago = today - timedelta(days=7)

    # Fetch all orders created in the last 7 days (including today)
    last_7_days_orders = vendor.orders.filter(created_at__date__gte=seven_days_ago)

    avg_order_sum = total_order.aggregate(total=Sum("subtotal"))["total"] or Decimal("0")
    total_orders = total_order.count()
    if total_orders:
        avg_order_sum = avg_order_sum / total_orders
    
    context={
        "vendor":vendor,
        "total_order":total_order,
        "avg_order_sum":avg_order_sum,
        "revenue":revenue,
        "previous_month_revenue":previous_month_revenue,
        "revenue_change":revenue_change,
        "current_month_name":today.strftime("%B"),
        "previous_month_name":previous_month_start.strftime("%B"),
        "last_7_days_orders":last_7_days_orders,
        "top_selling_items":top_selling_items,
        "media_url":settings.MEDIA_URL,
        "sales_chart": sales_chart,
    }
    return render(request,'vendor/v-dashboard.html',context)



@role_required("vendor")
def marketplace(request):
    vendors = VendorProfile.objects.all()
    context = {'vendors': vendors}
    return render(request,'vendor/v-dashboard.html',context)








