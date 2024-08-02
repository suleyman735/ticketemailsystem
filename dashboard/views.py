from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User
# Create your views here.

user = User()
@login_required
def dashboard(request):
    # return render(request,'dashboard/customer_dashboard.html')
    user = request.user
    if user.is_customer:
        return render(request,'dashboard/customer_dashboard.html')
    else:
        return render(request,'accounts/login.html')