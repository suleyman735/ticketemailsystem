from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField


User = get_user_model()

class Ticket(models.Model):
    
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='customer_tickets')
    engineer = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name='engineer',blank=True,null=True)
    ticket_id = models.CharField(max_length=15,unique=True)
    ticket_title = models.CharField(max_length=50)
    ticket_description = models.TextField()
    status = models.CharField(max_length=20,choices=(('Active','Active'),('Pending','Pending'), ('Resolved','Resolved')), default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    severity = models.CharField(max_length=5,choices=(('A','A'),('B','B')),default='B')
    # contact_mode = models.CharField(max_length=20,choices=(('Phone','Phone'),('Email','Email')))
    is_assigned_to_engineer = models.BooleanField(default=False)
    resolution_steps = models.TextField(blank=True,null=True)
# Create your models here.



class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField()  # Use CKEditor RichTextField instead of TextField
    sent_at = models.DateTimeField(auto_now_add=True)
    reply_to = models.EmailField(blank=True, null=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)  # Add attachment field



    def __str__(self):
        return f"Message by {self.sender} on {self.sent_at}"

    class Meta:
        ordering = ['sent_at']
