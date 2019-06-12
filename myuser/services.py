from django.core.mail import send_mail
from django.conf import settings
from .models import User

import random

def random_send(id,name):
    Msg = '''You have a job.
    The appliance no.'''+str(id)+''' is abnormal. 
    Please repair it in time.
    '''
    staffs = User.objects.filter(is_staff=True,is_superuser=False)
    staff = staffs[random.randint(0,len(staffs)-1)]
    #随机向员工发送邮件
    send_mail('Notice', Msg, settings.DEFAULT_FROM_EMAIL, staff.email)


def createcode():
    '''
    随机生成4位验证码
    '''
    list_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    list_str = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 's', 't', 'x', 'y',
                'z']
    veri_str = random.sample(list_str, 2)
    veri_num = random.sample(list_num, 2)
    veri_out = random.sample(veri_num + veri_str, 4)
    veri_res = str(veri_out[0]) + str(veri_out[1]) + str(veri_out[2]) + str(veri_out[3])
    return veri_res




