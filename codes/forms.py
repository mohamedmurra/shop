from django import forms
from .models import Code
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField

class CodeForm(forms.ModelForm):
 number = forms.CharField(label='Code',help_text ='Please wait, we are confirming your OTP')
 
 class Meta:
  model =Code
  fields =('number',)

class Creation_form(UserCreationForm):
 phone_number =PhoneNumberField()

 class Meta:
  model =CustomUser
  fields =('username','phone_number','password1','password2','email',)