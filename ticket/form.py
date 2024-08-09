from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Ticket,Message


class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_title','ticket_description']

        # 'contact_mode'
        
        
class AssignTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['engineer']
        
class MessageForm(forms.ModelForm):
    # body = forms.CharField(widget=CKEditorWidget())
    # # reply_to = forms.EmailField(required=False)
    attachment = forms.FileField(required=False)  # Add file field for attachments

    class Meta:
        model = Message
        fields = ['body', 'attachment']
        widgets = {
            'body': CKEditorWidget(),
        }