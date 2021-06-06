from django.db import models
from django.contrib.auth.models import AbstractUser 
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class CustomUser(AbstractUser):
 id =models.BigIntegerField(primary_key=True)
 phone_number =PhoneNumberField()


 
