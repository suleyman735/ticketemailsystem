from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_customer():
        return render(request,'dashboard/customer_dahsboard.html')
    # else:
    #     return render(request,'accounts/login.html')