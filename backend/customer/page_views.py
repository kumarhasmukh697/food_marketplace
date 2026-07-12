from django.shortcuts import render
from accounts.decorators import role_required



@role_required("customer")
def dashboard(request):
    print("path is : ",request.path)
    return render(request, "customer/dashboard.html")

