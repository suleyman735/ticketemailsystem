from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User
from ticket.models import Ticket
# Create your views here.

user = User()
@login_required
def dashboard(request):
    # return render(request,'dashboard/customer_dashboard.html')
    user = request.user
    if user.is_customer:
        tickets = Ticket.objects.filter(customer= user)
        active_tickets = Ticket.objects.filter(customer= user,is_resolved =False).count
        closed_tickets = Ticket.objects.filter(customer= user,is_resolved =True).count
        context = {'tickets':tickets,'active_tickets':active_tickets,'closed_tickets':closed_tickets}
        return render(request,'dashboard/customer_dashboard.html',context)
    elif user.is_engineer:
        tickets = Ticket.objects.filter(engineer= user)
        active_tickets = Ticket.objects.filter(engineer= user,is_resolved =False).count
        closed_tickets = Ticket.objects.filter(engineer= user,is_resolved =True).count
        context = {'tickets':tickets,'active_tickets':active_tickets,'closed_tickets':closed_tickets}
        return render(request,'dashboard/engineer_dashboard.html',context)
    elif user.is_superuser:
        
        tickets = Ticket.objects.all()
        print(tickets)
        active_tickets = Ticket.objects.filter(customer= user,is_resolved =False).count
        closed_tickets = Ticket.objects.filter(customer= user,is_resolved =True).count
        ticket_queue= Ticket.objects.filter(is_assigned_to_engineer = False)
        context = {'tickets':tickets,'active_tickets':active_tickets,'closed_tickets':closed_tickets,'tickets':tickets,'ticket_queue':ticket_queue}
        return render(request,'dashboard/admin_dashboard.html',context)
    

        
    # else:
    #     return render(request,'accounts/login.html')