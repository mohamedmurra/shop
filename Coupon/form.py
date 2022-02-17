from django import forms
from .models import Coupons


class coupon_form(forms.Form):
 code = forms.CharField(max_length=50)
