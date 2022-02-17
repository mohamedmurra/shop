from django.db import models
import random
import string
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


def tansaction_id_genrater():
  length = 8
  while True:
    code = ''.join(random.choices(string.hexdigits, k=length))
    if Coupons.objects.filter(code=code).count() == 0:
      break
  return code
class Coupons(models.Model):
 code = models.CharField(max_length=8,unique=True,default=tansaction_id_genrater)
 valid_from =models.DateTimeField()
 valid_to =models.DateTimeField()
 discount =models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
 active = models.BooleanField(default=False)

 def __str__(self):
   return self.code



