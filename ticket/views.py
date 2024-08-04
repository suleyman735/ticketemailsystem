import random
import string
from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.contrib import messages
from .form import CreateTicketForm,AssignTicketForm
from .models import Ticket


def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.ticket_id:
                id = ''.join(random.choices(string.digits,k=6))
                try:
                    var.ticket_id = id
                    var.save()          
                    messages.success(request,"Your ticket has been submitted, A support engineer would reach out soon")
                    return redirect('ticket:customer-active-tickets')
                   
                except IntegrityError:
                    continue
  
        else:
            messages.warning(request,"something went wrong. Please check form error")
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form':form}
        return render(request,'ticket/create_ticket.html',context)
    
# # def cx can see all created tickets
# def customer_tickets(request):
#     tickets = Ticket.objects.filter(customer=request.user).order_by('-created_on')
#     context = {'tickets':tickets}
#     return render(request,'ticket/customer_tickets.html',context)

# def cx can see all active tickets
def customer_active_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request,'ticket/customer_active_tickets.html',context)
# def cx can see all resolved tickets
def customer_resolved_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user,is_resolved=True).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request,'ticket/customer_resolved_tickets.html',context)
                   
        
def assign_ticket(request,ticket_id):
    ticket = Ticket.objects.get(ticket_id = ticket_id)
    if request.method =='POST':
        form = AssignTicketForm(request.POST,instance=ticket)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_engineer = True
            var.save()
            messages.success(request, f'Ticket has been assigned to {var.engineer}')
            return redirect('ticket-queue')
        else:
            messages.warning(request,'Someting went wrong. Please check form input')
            return redirect('assign-ticket')
    else:
        form =AssignTicketForm()
        context = {'form':form}
        return render(request,'ticket/assign_ticket.html',context)
    
def tickt_details(request,ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    context = {'ticket':ticket}
    return render(request,'ticket/ticket_details.html',context)

# ticket queue
def ticket_queue(request):
    ticket= Ticket.objects.filter(is_assigned_to_engineer = False)
    context = {'ticket':ticket}
    return render(request,'ticket/ticket_queue.html',context)



            
    
    
   

