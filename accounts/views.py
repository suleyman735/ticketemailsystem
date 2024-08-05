from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from .forms import RegisterCustomerForm


# Create your views here.

def register_customer(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        print(form)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_customer = True
            var.username = var.email
            var.save()
            messages.success(request,'Account created,Please login')
            return redirect('accounts:login')
        else:
            print(form.errors)
            messages.warning(request,'Something went wrong. Please check formerror')
            return redirect('accounts:register-customer')
    else:
        form = RegisterCustomerForm()
        context = {'form':form}
        return render(request, 'accounts/register_customer.html',context)
    
    
def login_user(request):
    print('hello')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        

        if user:
            login(request,user)
            return redirect('dashboard')
        else:
            print('Something went wrong. Please check form error')
            messages.warning(request,'Something went wrong. Please check form error')
            return redirect('accounts:login')
    else:
        return render(request,'accounts/login.html')
    

def logout_user(request):
    logout(request)
    messages.success(request,'Active session ended. Log in to continue')
    return redirect ('login')
    