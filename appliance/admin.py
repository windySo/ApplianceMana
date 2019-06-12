from django.contrib import admin
from .models import Appliance,Category
# Register your models here.

@admin.register(Appliance)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','depict','category','img',
                    'startValue','alertValue','min','max','status','created_time')


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('name','depict','index')
