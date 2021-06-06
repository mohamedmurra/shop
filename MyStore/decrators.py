from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_user(allowed_roles=[]):
 def decorator(view_func):
  def wrapper_func(request,*args, **kwargs):
   groub =None
   if request.user.groubs.exists():
    groub =request.user.groubs.exists()[0].name
    if groub in allowed_roles:
     return view_func(request,*args, **kwargs)
    else:
     return HttpResponse('u are not authorize to view this page')
  return wrapper_func
 return decorator