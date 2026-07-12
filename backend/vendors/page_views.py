from django.shortcuts import render
from accounts.decorators import role_required

@role_required("vendor")
def dashboard(request):
    return render(request,'vendor/v-dashboard.html')