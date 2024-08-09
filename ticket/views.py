import random
import string
from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .form import CreateTicketForm,AssignTicketForm,MessageForm
from .models import Ticket,Message
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

User = get_user_model()

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
              
                    # send email function    
                    # subject = f'{var.ticket_title} {var.ticket_id}' 
                    # message = 'Thank you for creating a ticket , we will assign an engineer soon' 
                    # from_email = f'{var.ticket_title} {var.ticket_id}<{settings.EMAIL_HOST_USER}>'
                    # recipient_list = [request.user.email]
                    # send_mail(subject,message,from_email,recipient_list)
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
def admin_tickets(request):
    tickets = Ticket.objects.all().order_by('-created_on')
    context = {'tickets':tickets}
    return render(request,'ticket/admin_tickets.html',context)
# def customer can see all active tickets
def customer_active_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request,'ticket/customer_active_tickets.html',context)
# def customer can see all resolved tickets
def customer_resolved_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user,is_resolved=True).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request,'ticket/customer_resolved_tickets.html',context)


# def engineer can see all active tickets
def engineer_active_tickets(request):
    tickets = Ticket.objects.filter(engineer=request.user, is_resolved=False).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request,'ticket/engineer_active_tickets.html',context)
# def engineer can see all resolved tickets
def engineer_resolved_tickets(request):
    tickets = Ticket.objects.filter(engineer=request.user,is_resolved=True).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request,'ticket/engineer_resolved_tickets.html',context)
                   
        
def assign_ticket(request,ticket_id):
    ticket = Ticket.objects.get(ticket_id = ticket_id)
    if request.method =='POST':
        form = AssignTicketForm(request.POST,instance=ticket)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_engineer = True
            var.status = 'Active'
            var.save()
            messages.success(request, f'Ticket has been assigned to {var.engineer}')
            return redirect('ticket:ticket-queue')
        else:
            messages.warning(request,'Someting went wrong. Please check form input')
            return redirect('ticket:assign-ticket')
    else:
        form =AssignTicketForm(instance=ticket)
        form.fields['engineer'].queryset = User.objects.filter(is_engineer = True)
        context = {'form':form,'ticket':ticket}
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

def resolve_ticket(request,ticket_id):
    print('tikxcskm')
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        print('tikxcskm')
        # rs = request.POST.get('rs')
        # ticket.resolution_steps = rs
        ticket.is_resolved = True
        ticket.status = 'Resolved'
        ticket.save()
        messages.success(request,'STicket is now resolved and closed')
        return redirect('dashboard')
        
        
        
def engineer_email(request,ticket_id):
    # page = get_object_or_404(Ticket, ticket_id=ticket_id)
    page = get_object_or_404(Message, ticket_id=ticket_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        # if form.is_valid():
        #     message = form.save(commit=False)
        #     message.ticket = ticket
        #     message.sender = request.user
        #     message.save()

        #     # Prepare email
        #     email = EmailMessage(
        #         subject=f"Re: [Ticket ID: {ticket.ticket_id}] {ticket.ticket_title}",
        #         body=message.content,
        #         from_email=request.user.email,
        #         to=[ticket.customer.email],
        #         reply_to=[message.reply_to] if message.reply_to else [request.user.email],
        #     )
            
        #     # Attach the file if it exists
        #     if message.attachment:
        #         email.attach(message.attachment.name, message.attachment.read(), message.attachment.content_type)
            
        #     # Send the email
        #     email.send(fail_silently=False)
            
        #     return JsonResponse({'status': 'success', 'message': 'Message sent successfully.'})
        # else:
        #     return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
        
    form1 =MessageForm(instance=page)
    # form.fields['engineer'].queryset = User.objects.filter(is_engineer = True)
    context = {'form1':form1,}
    # tickets = Ticket.objects.all().order_by('-created_on')
    # context = {'tickets':'tickets'}
    return render(request,'emails/engineer_email.html',context)



# @login_required
def post_message_view(request,  ticket_id):
    # ticket = get_object_or_404(Ticket, ticket_id=pk)
    if ticket_id:
        # Edit existing page
        page = get_object_or_404(Message, ticket_id=ticket_id)
    else:
        # Create new page
        page = None

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect('html_page_detail', ticket_id=page.ticket_id if page else form.instance.pk)
    else:
        form = MessageForm(instance=page)
    
    # if request.method == 'POST':
    #     form = MessageForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         message = form.save(commit=False)
    #         message.ticket = ticket
    #         message.sender = request.user
    #         message.save()

    #         # Prepare email
    #         email = EmailMessage(
    #             subject=f"Re: [Ticket ID: {ticket.ticket_id}] {ticket.ticket_title}",
    #             body=message.content,
    #             from_email=request.user.email,
    #             to=[ticket.customer.email],
    #             reply_to=[message.reply_to] if message.reply_to else [request.user.email],
    #         )
            
    #         # Attach the file if it exists
    #         if message.attachment:
    #             email.attach(message.attachment.name, message.attachment.read(), message.attachment.content_type)
            
    #         # Send the email
    #         email.send(fail_silently=False)
            
    #         return JsonResponse({'status': 'success', 'message': 'Message sent successfully.'})
    #     else:
    #         return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
        
    # form =MessageForm()
    # form.fields['engineer'].queryset = User.objects.filter(is_engineer = True)
    context = {'form':form,}
    
    return render(request,'emails/engineer_email.html',context)
            
    
    
   

