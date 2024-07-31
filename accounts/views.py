from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from .form import RegisterCustomerForm


# Create your views here.

def register_customer(request):
    if request.methot == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_customer = True
            var.username = var.email
            var.save()
            messages.success(request,'Account created,Please login')
            return redirect('login')
        else:
            messages.warning(request,'Something went wrong. Please check formerror')
            return redirect('register-customer')
    else:
        form = RegisterCustomerForm()
        context = {'form':form}
        return redirect(request, 'accounts/register_customer.html',context)
    
    
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password = password)
        
        if user is not None and user.is_active:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.warning(request,'Something went wrong. Please check form error')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')
    

def logout_user(request):
    logout(request)
    messages.success(request,'Active session ended. Log in to continue')
    return redirect ('login')
    