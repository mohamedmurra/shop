from django.shortcuts import render,redirect,get_object_or_404
from .models import blog, comment, Catagory
from account.models import Acount
from .forms import CommentForm ,Create_blog_post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from MyStore.utils import CartCoocies, cartData
from cloudinary.forms import cl_init_js_callbacks
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
    form = Create_blog_post()
  context = {'form': form}
  return render(request, 'home/add_blog.html', context=context)


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
  return render(request, 'home/update_blog.html', {'form': form, 'post': post})


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

  return render(request, 'blog/blog-single-page.html', {'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish,'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form,'count':counts})


def cata_fil(request, slug):
  data = cartData(request)
  cartItems = data['cartitems']
  items = data['items']
  order = data['order']
  wish = data['wish']
  popu =blog.objects.all()[:4]
  catagorys = Catagory.objects.all()
  blogs = blog.objects.filter(catagory__slug=slug)
  p = Paginator(blogs, 4)
  page_number = request.GET.get('page', 1)
  try:
    page_obj = p.get_page(page_number)
  except PageNotAnInteger:
    page_obj = p.page(1)
  except EmptyPage:
    page_obj = p.page(p.page_number)
  return render(request, 'blog/blog_filter.html', { 'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish, 'page_obj': page_obj, 'catagorys': catagorys,'popu':popu})

def blog_manage(request):
  blogs =blog.objects.all()
  return render(request,'home/blog_manage.html',{'blogs':blogs})