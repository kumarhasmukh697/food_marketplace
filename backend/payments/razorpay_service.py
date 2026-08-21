from decimal import Decimal
import razorpay
from django.conf import settings


class RazorpayService:

    def __init__(self):
        self.client = razorpay.Client(
            auth=( settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET,)
        )

    def create_order( self, amount, currency="INR", receipt=None, ):
        amount = Decimal(amount)
        amount_in_paise = int( amount * Decimal("100"))
        data = { "amount": amount_in_paise, "currency": currency,}

        if receipt:
            data["receipt"] = receipt

        return self.client.order.create( data=data)