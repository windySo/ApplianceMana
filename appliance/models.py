from django.db import models
from myuser.models import User

'''
数据库表结构的设计
'''

# Create your models here.
class Category(models.Model):
    '''
    仪器分类表 /// 暂时没有分类的需求
    '''
    name = models.CharField('类别',max_length=30)
    depict = models.TextField('描述',max_length=200,blank=True)
    index = models.IntegerField(default=999,verbose_name='分类排序')
    class Meta:
        verbose_name = '仪器分类'
        verbose_name_plural =verbose_name
    def __str__(self):
        return self.name

class Appliance(models.Model):
    '''
    仪器表
    '''
    STATUS_CHOICES =(
        ("normal","正常"),
        ("abnormal","异常")
    )
    name = models.CharField('仪器名称',max_length=30)
    depict = models.TextField('仪器描述',max_length=200,blank=True)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING,verbose_name='分类',blank=True,null=True)
    img = models.ImageField(upload_to='product/%Y/%m/%d',verbose_name='仪器图片',blank=True,null=True)
    startValue = models.DecimalField('状态值',max_digits=5,decimal_places=2,default=0.00)
    alertValue = models.DecimalField('阈值',max_digits=5,decimal_places=2,default=0.00)
    min = models.DecimalField('最小值',max_digits=5,decimal_places=2,default=0.00)
    max = models.DecimalField('最大值',max_digits=5,decimal_places=2,default=0.00)
    status = models.CharField('状态',max_length=10,choices=STATUS_CHOICES,default="normal")
    created_time = models.DateTimeField(verbose_name='生产时间',auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    class Meta:
        verbose_name = '仪器'
        verbose_name_plural = verbose_name


from django.db.models.signals import post_save
from django.dispatch import receiver
from myuser.services import random_send

@receiver(post_save, sender=Appliance)
def appliance_changed_signal(sender, instance, created, **kwargs):
    ''' 信号机制，当Appliance表改动时将会触发该函数，下同
    :param sender:
    :param instance: 被修改的 model对象实例 <class 'appliance.models.Appliance'>
    :param kwargs:
    '''
    if created:
        if instance.startValue>instance.alertValue:
            instance.status = "abnormal"
            Appliance.objects.filter(pk=instance.id).update(status="abnormal")
            random_send(instance.id, instance.name)

@receiver(post_save, sender=Appliance)
def appliance_changed_signal(sender, instance, **kwargs):

    if instance.startValue>instance.alertValue:
       Appliance.objects.filter(pk=instance.id).update(status="abnormal")
       random_send(instance.id,instance.name)
    else:
        Appliance.objects.filter(pk=instance.id).update(status="normal")




class Datacord(models.Model):
    '''
    数据变化记录表
    '''
    pid = models.ForeignKey(Appliance,related_name='data',on_delete=models.CASCADE,verbose_name='仪器',default='')
    value = models.DecimalField('状态值',max_digits=5,decimal_places=2,default=0.00)
    created_time = models.DateTimeField(verbose_name='时间',auto_now_add=True)
    class Meta:
        verbose_name = '修理记录'
        verbose_name_plural = verbose_name


class Repaircord(models.Model):
    '''
    修理记录表
    '''
    sid = models.ForeignKey(User,related_name='repair',on_delete=models.DO_NOTHING,verbose_name='维修人员',default='')
    pid = models.ForeignKey(Appliance,related_name='repair',on_delete=models.DO_NOTHING,verbose_name='损坏仪器',default='')
    accept_time = models.DateTimeField('受理时间',auto_now_add=True)
    finish_time = models.DateTimeField('维修成功时间',auto_now=True,null=True)
    is_finished = models.BooleanField('维修是否完成',default=False)
    class Meta:
        verbose_name = '修理记录'
        verbose_name_plural = verbose_name
