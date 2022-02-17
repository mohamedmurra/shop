from __future__ import unicode_literals,absolute_import

from celery import shared_task


@shared_task
def say_my_name():
 return print('iam the king bitch')