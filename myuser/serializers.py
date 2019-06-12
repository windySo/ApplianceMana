from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username','email','phone')




class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册
    '''
    username = serializers.CharField(label='用户名',
                                     required=True,
                                     allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message="用户已存在")])
    password = serializers.CharField(style={'input_type':'password'},
                                     write_only=True,
                                     required=True,label='密码')



    def create(self,validated_data):
        '''
        重写create（）方法实现密码加密
        :param validated_data:
        :return:
        '''
        user = super(UserRegSerializer,self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = User
        fields = ('id', 'username', 'password','is_staff', 'phone', 'email', )