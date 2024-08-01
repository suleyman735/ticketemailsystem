import random
import string
from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.contrib import messages
from .form import CreateTicketForm
from .models import Ticket


def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_Valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.ticket_id:
                id = ''.join(random.choice(string.digits,k=6))
                try:
                    var.ticket_id = id
                    var.save()
                    break
                except IntegrityError:
                    continue
            messages.success(request,"Your ticket has been submitted, A support engineer would reach out soon")
            return redirect('customer-tickets')
        else:
            messages.warning(request,"something went wrong. Please check form error")
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form':form}
        return redirect(request,'ticket/crate_ticket.html',context)
    
# def cx can see all created tickets
def customer_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user)
    context = {'tickets':tickets}
    return render(request,'ticket/customer_tickets.html',context)
                   
        
def assign_ticket(request):
    pass 

