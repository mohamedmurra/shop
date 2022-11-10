from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
# Create your models here.


def uplaod_lucation(instance, filename):
 file_path = 'blog/{author}/{title}-{filename}'.format(
     author=str(instance.author), title=str(instance.title), filename=filename
 )
 return file_path
 
class Catagory(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)

  def __str__(self):
    return self.name


class blog(models.Model):
 title = models.CharField(max_length=60, blank=False, null=False)
 body = RichTextField( blank=False, null=False)
 catagory =models.ForeignKey(Catagory,on_delete=models.SET_NULL,blank=True,null=True)
 image = CloudinaryField('image')
 date_published = models.DateTimeField(auto_now_add=True)
 date_updated = models.DateTimeField(auto_now=True)
 author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 slug = models.SlugField(blank=True, unique=True)

 class Meta:
    ordering = ('date_published',)

 def __str__(self):
  return self.title


@receiver(post_delete, sender=blog)
def delete_img(sender, instance, **kwargs):
 instance.image.delete(False)


def pre_save_reciver(sender, instance, *args, **kwargs):
 if not instance.slug:
  instance.slug = slugify(instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_reciver, sender=blog)


class comment(models.Model):
  post = models.ForeignKey(
      blog, on_delete=models.CASCADE, related_name='comments')
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  body = models.TextField(blank=True, null=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('created',)

  def __str__(self):
    return 'comment by {}'.format(self.body, self.user.username)
