from django.urls import path
from .views import *

app_name='ticket'

urlpatterns = [
path('create-ticket/', create_ticket, name='create-ticket'),
# path('customer-tickets/', customer_tickets, name='customer-tickets'),
path('customer-active-tickets/', customer_active_tickets, name='customer-active-tickets'),
path('customer-resolved-tickets/', customer_resolved_tickets, name='customer-resolved-tickets'),
path('assign-ticket/<str:ticket_id>/', assign_ticket, name='assign-ticket'),
path('ticket-details/<str:ticket_id>/', tickt_details, name='ticket-details'),
path('ticket-queue/', ticket_queue, name='ticket-queue'),
]
