from django.shortcuts import render
from accounts.decorators import role_required


@role_required("delivery")
def dashboard(request):
    return render(request,'delivery/dashboard.html')
