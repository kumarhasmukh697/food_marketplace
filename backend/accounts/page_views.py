from django.shortcuts import render


def home(request):
    return render(request,'home.html')

# register view
def register(request):
    return render(request,'accounts/register.html')

# login view
def login(request):
    return render(request,'accounts/login.html')

# verifyotp view
def verifyotp(request):
    return render(request,'accounts/verify-otp.html')

