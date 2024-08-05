

from .models import  transaction
from django import forms
import datetime

from django.contrib.auth.models import User
#    sender = forms.CharField(max_length=64)
  #  message= forms.CharField(max_length=64)
  
'''
class MessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
    
    class Meta:
        model = Message
        fields = ("__all__")
        widgets = {'sender': forms.HiddenInput()}
'''


class TransactionForm_sell(forms.ModelForm):

    class Meta:
        model = transaction
        fields = ("__all__")
        widgets = {'user': forms.HiddenInput(),'user_username': forms.HiddenInput(),'active': forms.HiddenInput(),'pp':forms.HiddenInput()}

class TransactionForm_buy(forms.Form):
    coin = forms.IntegerField()
    pk = forms.IntegerField(widget = forms.HiddenInput(), required = False)
    pp = forms.IntegerField(widget = forms.HiddenInput(), required = False)



