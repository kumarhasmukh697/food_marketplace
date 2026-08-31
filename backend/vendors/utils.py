import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from datetime import timedelta
from django.conf import settings
from django.utils import timezone


def generate_sales_chart(vendor):

    # ==========================================
    # DATE RANGE
    # ==========================================

    today = timezone.localdate()

    # Last 7 days including today
    start_date = today - timedelta(days=6)

    # ==========================================
    # VALID SALES STATUSES
    # ==========================================

    SALES_STATUSES = [
        "confirmed",
        "preparing",
        "ready",
        "picked_up",
        "out_for_delivery",
        "delivered",
    ]

    # ==========================================
    # GET VENDOR ORDERS
    # ==========================================

    orders = (
        vendor.orders
        .filter(
            created_at__date__gte=start_date,
            status__in=SALES_STATUSES
        )
        .prefetch_related("items")
    )

    # ==========================================
    # CREATE ALL 7 DAYS
    # ==========================================

    sales_by_day = {}

    for i in range(7):

        date = start_date + timedelta(days=i)

        sales_by_day[date] = 0

    # ==========================================
    # CALCULATE SALES
    # ==========================================

    for order in orders:

        order_date = order.created_at.date()

        for item in order.items.all():

            sales_by_day[order_date] += float(
                item.subtotal
            )

    # ==========================================
    # PREPARE CHART DATA
    # ==========================================

    dates = list(sales_by_day.keys())

    sales = list(sales_by_day.values())

    labels = [
        date.strftime("%a")
        for date in dates
    ]

    # ==========================================
    # CREATE FIGURE
    # ==========================================

    fig, ax = plt.subplots(
        figsize=(10, 4.5),
        dpi=120
    )

    # ==========================================
    # BACKGROUND
    # ==========================================

    fig.patch.set_facecolor("#f8fafc")

    ax.set_facecolor("#f8fafc")

    # ==========================================
    # CREATE BARS
    # ==========================================

    bars = ax.bar(
        labels,
        sales,
        width=0.55,
        color="#fb923c",
        edgecolor="none",
        zorder=3
    )

    # ==========================================
    # DISPLAY VALUE ABOVE EACH BAR
    # ==========================================

    for bar in bars:

        height = bar.get_height()

        if height > 0:

            ax.annotate(
                f"₹{height:,.0f}",
                xy=(
                    bar.get_x() + bar.get_width() / 2,
                    height
                ),
                xytext=(0, 7),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
                color="#475569"
            )

    # ==========================================
    # RUPEE FORMATTER
    # ==========================================

    def rupee_formatter(value, position):

        if value >= 100000:

            return f"₹{value / 100000:.1f}L"

        elif value >= 1000:

            return f"₹{value / 1000:.0f}K"

        else:

            return f"₹{value:.0f}"

    ax.yaxis.set_major_formatter(
        FuncFormatter(rupee_formatter)
    )

    # ==========================================
    # GRID
    # ==========================================

    ax.grid(
        axis="y",
        linestyle="-",
        linewidth=0.8,
        color="#f7ac70",
        alpha=0.8,
        zorder=0
    )

    ax.grid(
        axis="x",
        visible=False
    )

    # ==========================================
    # REMOVE SPINES
    # ==========================================

    ax.spines["top"].set_visible(False)

    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_visible(False)

    ax.spines["bottom"].set_visible(False)

    # ==========================================
    # X AXIS
    # ==========================================

    ax.tick_params(
        axis="x",
        colors="#01060c",
        labelsize=10,
        length=0,
        pad=10
    )

    # ==========================================
    # Y AXIS
    # ==========================================

    ax.tick_params(
        axis="y",
        colors="#01060c",
        labelsize=9,
        length=0,
        pad=8
    )

    # ==========================================
    # REMOVE AXIS LABEL
    # ==========================================

    ax.set_ylabel("")

    # ==========================================
    # Y AXIS RANGE
    # ==========================================

    max_sales = max(sales)

    if max_sales > 0:

        ax.set_ylim(
            0,
            max_sales * 1.20
        )

    else:

        ax.set_ylim(
            0,
            100
        )

    # ==========================================
    # LAYOUT
    # ==========================================

    plt.tight_layout(
        pad=1.5
    )

    # ==========================================
    # CREATE CHART DIRECTORY
    # ==========================================

    chart_dir = os.path.join(
        settings.MEDIA_ROOT,
        "charts"
    )

    os.makedirs(
        chart_dir,
        exist_ok=True
    )

    # ==========================================
    # CHART FILE PATH
    # ==========================================

    chart_path = os.path.join(
        chart_dir,
        f"vendor_{vendor.id}_sales.png"
    )

    # ==========================================
    # SAVE IMAGE
    # ==========================================

    plt.savefig(
        chart_path,
        dpi=120,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )

    plt.close(fig)

    # ==========================================
    # RETURN IMAGE URL
    # ==========================================

    return (
        f"{settings.MEDIA_URL}"
        f"charts/vendor_{vendor.id}_sales.png"
    )