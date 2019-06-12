from rest_framework import serializers
from .models import Category,Appliance,Repaircord
from myuser.serializers import UserSerializer

'''
Model 序列化类设计
'''

class ApplianceAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        #fields 指定序列化的字段 使用'__all__'序列化所有字段
        fields = ('id','name','depict','startValue','alertValue','min','max','status','created_time')

class AppUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = ('id','name','depict','startValue','alertValue',)


class RepaircordSerializer(serializers.ModelSerializer):
    sid = UserSerializer(read_only=True)
    pid = ApplianceAddSerializer(read_only=True)
    class Meta:
        model = Repaircord
        fields = ('id','sid','pid','accept_time','finish_time','is_finished')
        depth = 1
