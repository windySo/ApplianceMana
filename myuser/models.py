from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User (AbstractUser):
    '''
    User 用户表，对Django系统的AbstractUser进行扩展
    '''
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11,unique=True,null=True,blank=True)
    icon = models.ImageField('头像',upload_to='icon/%Y/%m/%d',blank=True)
    profile = models.TextField('个人简介',max_length=200,blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username