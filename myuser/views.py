from django.core.mail import send_mail
from django.views import View
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer,UserRegSerializer
from .services import createcode
from django.core.cache import cache
from django.conf import settings
import json
# Create your views here.


import logging
logger = logging.getLogger("user:views")

class MyPageNumber(PageNumberPagination):
    page_size = 5  # 每页显示多少条
    page_size_query_param = 'size'  # URL中每页显示条数的参数
    page_query_param = 'page'  # URL中页码的参数
    max_page_size = None  # 最大页码数限制

# 用户列表 GET  /user/all/
class UserList(APIView):
    def get(self,request):
     users = User.objects.all()
     total = users.count()
     page_obj = MyPageNumber()
     page_users = page_obj.paginate_queryset(queryset=users, request=request, view=self)
     serialzer = UserSerializer(page_users, many=True)
     dict = {'code': 0, 'msg': "返回信息成功", }
     dict['total'] = total
     dict['data'] = serialzer.data
     return HttpResponse(json.dumps(dict), content_type='application/json')

# 用户搜索 POST  /user/inquire/
class UserSearch(APIView):
    def post(self,request):
        email = request.data.get('email')
        users = User.objects.filter(email__icontains=email)
        total = users.count()
        page_obj = MyPageNumber()
        page_users = page_obj.paginate_queryset(queryset=users, request=request, view=self)
        serialzer = UserSerializer(page_users, many=True)
        dict = {'code': 0, 'msg': "返回信息成功", }
        dict['total'] = total
        dict['data'] = serialzer.data
        return HttpResponse(json.dumps(dict), content_type='application/json')

# 删除用户 POST /user/delete
class UserDelete(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def post(self,request):
        print(request.auth)
        print('user',request.user)
        req=request.data
        id = req.get('id')
        dict = {
            'code':"",
            'msg':"",
            'user':request.user.username
        }
        try:
            user = User.objects.get(pk=id)
            dict['code']="0"
            dict['msg'] = "删除用户成功"
        except Exception  as e:
            logger.exception("Exception in /user/delete")
            dict['code']="-1"
            dict['msg']="删除用户失败 : "+str(e)
        return HttpResponse(json.dumps(dict),content_type='application/json')


#  发送验证码  POST /public/email
class CodeSend(View):
    def post(self,request):
        email =request.POST.get('email')
        logger.info("email:"+email)
        dict = {"code":"-1","msg":""}
        captcha = createcode()
        cache.set('captcha',captcha,60*1)
        print(cache.get('captcha'))
        Msg = '验证码：' + captcha
        try:
            send_mail('邮箱验证', Msg, settings.DEFAULT_FROM_EMAIL, [email,])
            dict['code']=0
            dict['msg']="邮件已发送，请注意查收"
        except Exception as e:
            logger.exception("Exception in /public/email")
            dict['code'] = -1
            dict['msg'] = "邮件发送失败"+str(e)

        return HttpResponse(json.dumps(dict),content_type='application/json')

#  用户注册 POST  /sign/register/
class RegisterView2(APIView):
    def post(self,request):
        captcha = cache.get('captcha')
        serializer = UserRegSerializer(data=request.data)
        dict = {
            'code': "",
            'msg': "",
        }
        if  captcha == request.data.get("code"):

            if serializer.is_valid():
                u=serializer.save()
                dict['code'] = 0
                dict['msg'] = '注册成功'
            else:
                dict['code'] = -1
                dict['msg'] = '该邮箱/用户名已被占用'
        else:
            dict['code'] = -1
            dict ['msg'] = '验证码错误'
        return HttpResponse(json.dumps(dict),content_type='application/json')

#  修改信息  POST  user/change/
class InfoChange(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def post(self,request):
        user = request.user
        name = request.data.get('name')
        phone=request.data.get('phone')
        password = request.data.get('passward')
        rsp = {
            'code': -1,
            'msg': "",
        }
        try:
            if phone != None :
                user.phone=phone
            if name != None:
                user.username = name
            if password != None:
                user.set_password(password)
            user.save()
            rsp['code']= 0
            rsp['msg']="更新信息成功"
        except Exception as e:
            logger.exception("Exception in /user/update")
            rsp['code']=-1
            rsp['msg']= "更新失败"
        return HttpResponse(json.dumps(rsp),content_type='application/json')



