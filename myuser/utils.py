from django.contrib.auth.backends import ModelBackend
from .models import User
import re
import logging


logger = logging.getLogger("user:utils")


def jwt_response_playload_handler(token,user=None,request=None):
    '''
    自定义JWT返回数据
    '''
    return {
        'token':token,
        'user_id':user.id,
        'username':user.username
    }


def get_user_account(account):
    try:
        if re.match('^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',account):
            # 判断获取的account是邮箱/用户名
            user = User.objects.get(email=account)
        else:
            user=User.objects.get(username=account)
    except User.DoesNotExist:
        logger.exception("User Does Not Exist")
        return  None
    return user


class UsernameMobileAuthBackend(ModelBackend):
    '''自定义用户认证后台，用户可通过email/username之一进行认证'''
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_account(username)
        if user:
            if user.check_password(password):
                """如果用户密码校验成功，返回用户模型对象"""
            return user
        else:
            return None
