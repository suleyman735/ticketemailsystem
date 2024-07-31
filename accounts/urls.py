from django.urls import path
from .views import *

app_name='accounts'

urlpatterns = [
path('register-customer/', register_customer, name='register-customer'),
path('login/', login, name='login'),
path('logout/', logout, name='logout'),

]
