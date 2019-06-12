from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from myuser.services import random_send
from .models import Appliance,Repaircord,Datacord
from .serializers import ApplianceAddSerializer,RepaircordSerializer,AppUpdateSerializer
import json

# Create your views here.


# 日志处理
import logging
logger = logging.getLogger("appliance:"+__name__)

#分页设置
class MyPageNumber(PageNumberPagination):
    page_size = 5  # 每页显示多少条
    page_size_query_param = 'size'  # URL中每页显示条数的参数
    page_query_param = 'page'  # URL中页码的参数
    max_page_size = None  # 最大页码数限制



class ApplianceList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  #设置登录权限
    authentication_classes = (JSONWebTokenAuthentication,)  #使用JWT认证方式
    def get(self,request):     # GET  /appliance/all
        logger.info("aaa")
        appliances= Appliance.objects.all()
        total = appliances.count()
        page_obj = MyPageNumber()
        page_appliances = page_obj.paginate_queryset(queryset=appliances, request=request, view=self)
        serialzer = ApplianceAddSerializer(page_appliances,many=True)
        dict = {'code':0, 'msg':"返回信息成功", }
        dict['total'] = total
        dict['data']=serialzer.data
        return HttpResponse(json.dumps(dict),content_type='application/json')
    def post(self,request,format=None):   # POST /appliance/add
        serializer = ApplianceAddSerializer(data=request.data)
        dict = {'code': "", 'msg': "",}
        if serializer.is_valid():
            serializer.save()
            dict['code'] = "0"
            dict['msg'] = "添加仪器成功"
        else:
            dict['code'] = "-1"
            dict['msg'] = "添加仪器失败"
        return HttpResponse(json.dumps(dict),content_type='application/json')

# POST /appliance/inquire
class ApplianceSearch(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def post(self,request):
        name = request.data.get('name')
        appliances = Appliance.objects.filter(name__icontains=name)
        total = appliances.count()
        page_obj = MyPageNumber()
        page_appliances = page_obj.paginate_queryset(queryset=appliances, request=request, view=self)
        serialzer = ApplianceAddSerializer(page_appliances,many=True)
        dict = {'code': 0, 'msg': "返回信息成功", }
        dict['total'] = total
        dict['data'] = serialzer.data
        return HttpResponse(json.dumps(dict), content_type='application/json')


# POST /appliance/data/
class ApplianceData(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def post(self,request,format=None):
        pid = request.data.get('id')
        dict = {'code': 0, 'msg': "返回信息成功", }
        try:
            appliance = Appliance.objects.get(id=pid)
            datas = Datacord.objects.filter(pid=appliance)
            total = datas.count()
            if total>20:
                datas = datas[total-20:total]
            data = []
            for x in datas:
                data.append(float(x.value))
            dict['total'] = (total if (total<20) else 20)
            dict['data'] = data
        except Exception as e:
            dict['code'] = -1
            dict['msg'] = "返回数据失败：" + str(e)
            logger.exception(e)
        return HttpResponse(json.dumps(dict), content_type='application/json')


#  删除仪器 POST /appliance/delete
class ApplianceDelete(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def post(self,request):
        id = request.data.get("id")
        dict = {
            'code': "",
            'msg': "",
        }
        try:
            Appliance.objects.get(pk=id).delete()
            dict['code'] = "0"
            dict['msg'] = "删除仪器成功"
        except Exception as e:
            logger.exception(e)
            dict['code'] = "-1"
            dict['msg'] = "删除仪器失败 : " + str(e)
        return HttpResponse(json.dumps(dict),content_type='application/json')

#  编辑仪器信息 POST /appliance/update
class ApplianceUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def post(self,request):
        id = request.data.get('id')
        product = Appliance.objects.get(id=id)
        serializer = AppUpdateSerializer(product, data=request.data)
        dict = { 'code':'', 'msg':"" }
        if serializer.is_valid():
            serializer.save()
            dict['code'] = "0"
            dict['msg'] = "修改仪器成功"
        else:
            dict['code'] = "-1"
            dict['msg'] = "修改仪器失败"
        return HttpResponse(json.dumps(dict), content_type='application/json')

# 查看维修记录 GET  record/
class RepaircordView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def get(self, request):
        user = request.user
        repaircords = Repaircord.objects.filter(sid=user)
        total = repaircords.count()
        page_obj = MyPageNumber()
        page_records = page_obj.paginate_queryset(queryset=repaircords, request=request, view=self)
        serialzer = RepaircordSerializer(page_records,many=True)
        dict = {'code': 0, 'msg': "返回信息成功", }
        dict['data'] = serialzer.data
        dict['total'] = total
        return HttpResponse(json.dumps(dict), content_type='application/json')

# 搜索维修记录 GET  record/inquire/
class RepairSearch(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def post(self, request):
        user = request.user
        name = request.data.get('name')
        repaircords = Repaircord.objects.filter(sid=user,pid__name__icontains=name)
        total = repaircords.count()
        page_obj = MyPageNumber()
        page_records = page_obj.paginate_queryset(queryset=repaircords, request=request, view=self)
        serialzer = RepaircordSerializer(page_records,many=True)
        dict = {'code': 0, 'msg': "返回信息成功", }
        dict['data'] = serialzer.data
        dict['total'] = total
        return HttpResponse(json.dumps(dict), content_type='application/json')


# 维修仪器 POST record/inquire/
class HandleView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def post(self,request):
        dict = {
            'code': '',
            'msg': ""
        }
        pid = int(request.data.get('id'))
        value = float(request.data.get('startValue'))
        appliance = Appliance.objects.get(id=pid)
        Repaircord.objects.create(pid=appliance, sid=request.user,is_finished=True)
        appliance.startValue = value
        appliance.save()
        Datacord.objects.create(pid=appliance, value=appliance.startValue)
        dict['code'] = "0"
        dict['msg'] = "修改仪器成功"
        return HttpResponse(json.dumps(dict), content_type='application/json')





# 定时任务
import random
from apscheduler.schedulers.background import  BackgroundScheduler
from django_apscheduler.jobstores import  DjangoJobStore,register_events,register_job

scheduler = BackgroundScheduler()
try:
    scheduler.add_jobstore(DjangoJobStore(),"default"),
    # ('scheduler',"interval", seconds=1)  #用interval方式循环，每30min执行一次
    @register_job(scheduler, 'interval', minutes=30, id='task_time')
    def check_job():
        # 每隔30min 从数据库中查询 状态为normal的仪器，修改当前值
        appliances = Appliance.objects.filter(status='normal')
        for x in appliances:
            min = x.min
            max = x.max
            value = random.randint(min, max)
            x.startValue = value
            x.save()
            Datacord.objects.create(pid=x, value=x.startValue)


    @register_job(scheduler,'interval',hours=6,id='task_time2')
    def email_job():
        # 每隔30min 从数据中查询状态为abnormal的仪器，随机向员工发生邮件提醒维修
        appliances = Appliance.objects.filter(status='abnormal')
        for x in appliances:
            random_send(x.id, x.name)
    # 监控任务
    register_events(scheduler)
    # 调度器开始
    scheduler.start()
except Exception as e:
    logger.exception("Exception in Apscheduler")
    scheduler.shutdown()







