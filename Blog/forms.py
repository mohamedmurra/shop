from account.models import Acount
from .models import Catagory, comment, blog
from django import forms


class CommentForm(forms.ModelForm):
  user = comment.user

  class Meta:
    model = comment
    fields = ('body',)


class Create_blog_post(forms.ModelForm):
  class Meta:
    model = blog
    fields = ['title', 'body', 'image','catagory']

class Create_catagory(forms.ModelForm):
  class Meta:
    model = Catagory
    fields = '__all__'

