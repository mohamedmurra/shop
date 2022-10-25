from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import blog, comment, Catagory
from account.models import Acount
from .forms import CommentForm ,Create_blog_post, Create_catagory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from MyStore.utils import CartCoocies, cartData
# Create your views here.


def homepage(request):
  
  data = cartData(request)
  cartItems = data['cartitems']
  items = data['items']
  order = data['order']
  wish = data['wish']
  catagorys = Catagory.objects.all()
  popu =blog.objects.all()[:4]
  blogs = blog.objects.all()
  p = Paginator(blogs, 4)
  page_number = request.GET.get('page', 1)
  try:
    page_obj = p.get_page(page_number)
  except PageNotAnInteger:
    page_obj = p.page(1)
  except EmptyPage:
    page_obj = p.page(p.page_number)
  return render(request, 'blog/blog.html', { 'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish, 'page_obj': page_obj, 'catagorys': catagorys,'popu':popu})

def create_catagory(request):
  if not request.user.is_authenticated:
    return redirect('login')
  cata =Catagory.objects.all()
  form = Create_catagory(request.POST or None, request.FILES or None)
  if form.is_valid():
     form.save()
  context = {'form': form,'cata':cata}
  return render(request, 'panel/add_blog_catagory.html', context=context)


def create_blog_view(request):
  if not request.user.is_authenticated:
    return redirect('login')
  user = request.user
  form = Create_blog_post(request.POST or None, request.FILES or None)
  if form.is_valid():
    obj = form.save(commit=False)
    author = Acount.objects.filter(email=user.email).first()
    obj.author = author
    obj.save()
    return redirect('blog_manage')
  context = {'form': form}
  return render(request, 'panel/add_blog.html', context=context)


def update_catagory(request, slug):
  if not request.user.is_authenticated:
    return redirect('login')
  cata = get_object_or_404(Catagory, slug=slug)
  form = Create_catagory(request.POST or None,
                         request.FILES or None, instance=cata)
  if request.method == 'POST':
      if form.is_valid():
        form.save()
        return redirect('add_blog_Catagory')
  return render(request, 'panel/update_blog_catagory.html', {'form': form, 'cata': cata})


def update_blog_view(request, slug):
  if not request.user.is_authenticated:
    return redirect('login')
  user = request.user
  post = get_object_or_404(blog, slug=slug)
  if post.author == request.user:
    form = Create_blog_post(request.POST or None,
                            request.FILES or None, instance=post)
    if request.method == 'POST':
      if form.is_valid():
        obj = form.save(commit=False)
        author = Acount.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
  else:
    return redirect('blog_manage')
  return render(request, 'panel/update_blog.html', {'form': form, 'post': post})

def delete_catagory(request, slug):
  if not request.user.is_authenticated:
    return redirect('login')
  cata = get_object_or_404(Catagory, slug=slug)
  if request.user.is_admin:
    cata.delete()
  elif request.user.is_superuser :
    cata.delete()
  else:
    return redirect('add_blog_Catagory')
  return redirect('add_blog_Catagory')

def delete_blog_view(request, slug):
  if not request.user.is_authenticated:
    return redirect('login')
  user = request.user
  post = get_object_or_404(blog, slug=slug)
  if post.author == request.user:
    post.delete()
  elif request.user.is_superuser :
    post.delete()
  else:
    return redirect('blog_manage')
  return redirect('blog_manage')


def post_detail(request, slug):
  data = cartData(request)
  cartItems = data['cartitems']
  items = data['items']
  order = data['order']
  wish = data['wish']
  post = get_object_or_404(blog, slug=slug)
  comments = post.comments.all()
  counts =comments.count()
  comment_form = CommentForm()
  new_comment = None
  if request.method == 'POST':
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      parent_id = None
      try:
        parent_id = int(request.POST.get('parent_id'))
      except:
        parent_id = None
      if parent_id:
        parent_obj = comments.objects.get(id=parent_id)
        if parent_obj:
          replay_comment = CommentForm.save(commit=False)
          replay_comment.user = request.user
          replay_comment.parent = parent_obj
      new_comment = comment_form.save(commit=False)
      new_comment.post = post
      new_comment.user = request.user
      new_comment.save()
      return redirect(reverse('post_detail',args=[post.slug]))

  return render(request, 'blog/blog-single-page.html', {'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish,'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form,'count':counts})


def cata_fil(request, slug):
  data = cartData(request)
  cartItems = data['cartitems']
  items = data['items']
  order = data['order']
  wish = data['wish']
  popu =blog.objects.all()[:4]
  catagorys = Catagory.objects.all()
  blog_name =Catagory.objects.get(slug=slug)
  blogs = blog.objects.filter(catagory__slug=slug)
  p = Paginator(blogs, 4)
  page_number = request.GET.get('page', 1)
  try:
    page_obj = p.get_page(page_number)
  except PageNotAnInteger:
    page_obj = p.page(1)
  except EmptyPage:
    page_obj = p.page(p.page_number)
  return render(request, 'blog/blog_filter.html', { 'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish, 'page_obj': page_obj, 'catagorys': catagorys,'popu':popu,'blog_name':blog_name,'popular':blogs[:3]})
@login_required()
def blog_manage(request):
  blogs =blog.objects.all()
  return render(request,'panel/blog_manage.html',{'blogs':blogs})