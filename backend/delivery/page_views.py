from django.shortcuts import render
from orders.models import Order
from accounts.decorators import role_required


@role_required("delivery")
def dashboard(request):

    delivery_partner = request.user.delivery_partner

    assigned_orders = Order.objects.filter(
        delivery_partner=delivery_partner
    ).select_related(
        "customer",
        "customer__address",
        "vendor",
        "vendor__user",
        "vendor__user__address",
    ).prefetch_related(
        "items__product"
    ).order_by("-created_at")

    new_orders = assigned_orders.filter(
        status="ready"
    )

    active_orders = assigned_orders.filter(
        status__in=[
            "picked_up",
            "out_for_delivery",
        ]
    )
    print("NEW",new_orders)
    print("ASSIGNED",assigned_orders)
    print("ACTIVE",active_orders)
    completed_orders = assigned_orders.filter(
        status="delivered"
    )

    context = {
        "assigned_orders": assigned_orders,
        "new_orders": new_orders,
        "active_orders": active_orders,
        "completed_orders": completed_orders,
    }

    return render(
        request,
        "delivery/dashboard.html",
        context
    )