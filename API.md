
# 仪器监控预警API文档

### 基本返回格式
```
{
     "code": 0 /-1,
     "data":{
     返回数据内容
     },
     "msg":"错误信息"   
 }
```

| code | 描述    |
|------|---------|
|0     |请求成功 |
|-1    |请求失败 |


### **一. 用户模块**
#### 1.  获取验证码

请求url：` public/email/`

请求方式：POST

请求参数：

- email：邮箱地址

返回数据
```json
{
    "code": 0,
    "msg": "邮件已发送，请注意查收"
}
```
*说明：后台向用户输入的邮箱发送邮件，验证码在邮件正文中。*
#### 2.  用户注册
请求url：` sign/register/`

请求方式：POST

请求参数： 

- username：用户名
- password：密码
- email：邮箱
- code：验证码
- phone：电话号码
- is_staff:是否为管理员（默认为True）

返回数据
```json
{
    "code": 0,
    "msg": "注册成功"
}
```
#### 3.  用户登录
请求url：` sign/login/`

请求方式：POST

请求参数：

- username：用户名
- password：密码

返回数据
```json
{
    "user_id": 3,
    "username": "worker2",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ijk5MzYyNjU0N0BxcS5jb20iLCJleHAiOjE1NjA0Mzk0MjAsInVzZXJfaWQiOjMsInVzZXJuYW1lIjoid29ya2VyMiJ9.Kg9Apy8yOP1nl6dzkNGO1D2P8q-gN8SWc3WVjjrOdlA",
}
```
*说明：用户拿到token作为HTTP请求首部，用于后续的权限验证。*
#### 4.  获取用户列表
请求url：` user/all/`

请求方式：GET

请求参数：

-  page：页数
- size：每页大小

返回数据
```
{
    "data": [
        {
            "id": 1,
            "username": "admin",
            "email": "13102813385@163.com",
            "phone": null
        },
        {
            "id": 2,
            "username": "modifyname",
            "email": "2501165414@qq.com",
            "phone": null
        },
        {
            "id": 3,
            "username": "worker2",
            "email": "993626547@qq.com",
            "phone": "13101813385"
        },
        {
            "id": 4,
            "username": "huangdongxv",
            "email": "1323178720@qq.com",
            "phone": "123123"
        },
        {
            "id": 5,
            "username": "worker0",
            "email": "99362654@qq.com",
            "phone": "13102813385"
        }
    ],
    "code": 0,
    "total": 8,
    "msg": "返回信息成功"
}
```
#### 5.  根据邮箱查询用户
请求url：` user/inquire/`

请求方式：POST

请求参数：

- email：邮箱关键字
- page: 页数
- size：每页大小

返回数据
```
{
    "data": [
        {
            "id": 3,
            "username": "worker2",
            "email": "993626547@qq.com",
            "phone": "13101813385"
        },
        {
            "id": 5,
            "username": "worker0",
            "email": "99362654@qq.com",
            "phone": "13102813385"
        },
        {
            "id": 7,
            "username": "罗",
            "email": "767199722@qq.com",
            "phone": "13258236260"
        }
    ],
    "code": 0,
    "total": 3,
    "msg": "返回信息成功"
}
```
#### 6.  修改用户信息
请求url：` user/update/`

请求方式：POST

请求参数：

- name:用户名（可选）
- phone：电话（可选）
- password：密码（可选）

返回数据
```
{
    "code": 0,
    "msg": "更新信息成功"
}
```

### **二. 仪器管理模块**
#### 1.  获取仪器列表
请求url：` appliance/all/`

请求方式：GET

请求参数：

- page：页数
- size：每页大小

返回数据
```
{
    "data": [
        {
            "id": 1,
            "name": "温度检测装置",
            "depict": "监控当前生产环境的温度。",
            "startValue": "17.00",
            "alertValue": "30.00",
            "min": "0.00",
            "max": "20.00",
            "status": "normal",
            "created_time": "2019-04-28T04:37:27.674435"
        },
        {
            "id": 3,
            "name": "湿度检测装置",
            "depict": "监控当前生产环境的湿度。",
            "startValue": "2.00",
            "alertValue": "44.00",
            "min": "0.00",
            "max": "10.00",
            "status": "normal",
            "created_time": "2019-04-28T04:42:56.401269"
        },
        {
            "id": 4,
            "name": "紫外检测装置",
            "depict": "监控当前生产环境的紫外线照射程度。",
            "startValue": "0.00",
            "alertValue": "12.00",
            "min": "0.00",
            "max": "0.00",
            "status": "normal",
            "created_time": "2019-04-28T05:31:16.119285"
        },
        {
            "id": 5,
            "name": "生产仪器a",
            "depict": "用于a物品的生产。",
            "startValue": "30.00",
            "alertValue": "99.00",
            "min": "0.00",
            "max": "100.00",
            "status": "normal",
            "created_time": "2019-06-03T14:59:45.972606"
        },
        {
            "id": 6,
            "name": "生产仪器b",
            "depict": "用于b物品的生产。",
            "startValue": "37.00",
            "alertValue": "23.00",
            "min": "3.00",
            "max": "40.00",
            "status": "abnormal",
            "created_time": "2019-06-03T15:21:10.308231"
        }
    ],
    "code": 0,
    "total": 10,
    "msg": "返回信息成功"
}
```
#### 2.  根据仪器名称查询仪器
请求url：` appliance/inquire/`

请求方式：POST

请求参数：

- name：邮箱关键字
- page:页数
- size：每页大小

返回数据
```
{
    "data": [
        {
            "id": 7,
            "name": "Flask",
            "depict": "this is a flask",
            "startValue": "25.00",
            "alertValue": "23.00",
            "min": "0.00",
            "max": "100.00",
            "status": "abnormal",
            "created_time": "2019-06-05T15:50:17.889283"
        },
        {
            "id": 10,
            "name": "Flask2",
            "depict": "this is a flask",
            "startValue": "35.00",
            "alertValue": "25.00",
            "min": "0.00",
            "max": "100.00",
            "status": "abnormal",
            "created_time": "2019-06-09T14:24:51.556251"
        },
        {
            "id": 11,
            "name": "Flask4",
            "depict": "this is a flask",
            "startValue": "80.00",
            "alertValue": "25.00",
            "min": "0.00",
            "max": "100.00",
            "status": "abnormal",
            "created_time": "2019-06-09T14:28:11.092830"
        }
    ],
    "code": 0,
    "total": 3,
    "msg": "返回信息成功"
}
```
#### 3.  添加仪器
请求url：` appliance/add/`

请求方式：POST

请求参数：

- name
- depict
- startValue
- alertValue
- min
- max

返回数据
```
{
    "code": 0,
    "msg": "添加仪器成功"
}
```
#### 3.  删除仪器
请求url：` appliance/delete/`

请求方式：POST

请求参数：

- id

返回数据
```
{
    "code": 0,
    "msg": "删除仪器成功"
}
```
#### 4.  获取仪器近20条数据
请求url：` appliance/data/`

请求方式：POST

请求参数：

- id

返回数据
```
{
    "data":[8.0, 18.0, 11.0, 11.0, 11.0, 11.0, 11.0, 13.0, 3.0, 19.0, 11.0, 15.0, 12.0, 1.0, 3.0, 2.0, 11.0, 0.0, 15.0, 17.0]
    "code": 0,
    "total": 20,
    "msg": "返回信息成功"
}
```
#### 5.  修改仪器信息
请求url：` appliance/update/`
请求方式：POST
请求参数：

- name
- depict
- startValue
- alertValue
- min
- max

返回数据
```
{
    "code": 0,
    "msg": "修改仪器成功"
}
```

#### 6.  维修报警仪器
请求url：` handle/`

请求方式：POST

请求参数：

- id
- startValue

返回数据
```
{
    "code": 0,
    "msg": "维修仪器成功"
}
```

#### 7. 获取用户维修记录
请求url：` record/`

请求方式：GET

请求参数：

- page
- size

返回数据
```
{
    "data": [
        {
            "id": 3,
            "sid": {
                "id": 3,
                "username": "worker2",
                "email": "993626547@qq.com",
                "phone": "13101813385"
            },
            "pid": {
                "id": 5,
                "name": "生产仪器a",
                "depict": "用于a物品的生产。",
                "startValue": "11.00",
                "alertValue": "99.00",
                "min": "0.00",
                "max": "100.00",
                "status": "normal",
                "created_time": "2019-06-03T14:59:45.972606"
            },
            "accept_time": "2019-06-05T12:41:47.442270",
            "finish_time": "2019-06-09T14:08:09.178199",
            "is_finished": true
        },
        {
            "id": 4,
            "sid": {
                "id": 3,
                "username": "worker2",
                "email": "993626547@qq.com",
                "phone": "13101813385"
            },
            "pid": {
                "id": 7,
                "name": "Flask",
                "depict": "this is a flask",
                "startValue": "25.00",
                "alertValue": "23.00",
                "min": "0.00",
                "max": "100.00",
                "status": "abnormal",
                "created_time": "2019-06-05T15:50:17.889283"
            },
            "accept_time": "2019-06-05T15:50:27.053431",
            "finish_time": "2019-06-05T15:50:27.053490",
            "is_finished": true
        },
        {
            "id": 5,
            "sid": {
                "id": 3,
                "username": "worker2",
                "email": "993626547@qq.com",
                "phone": "13101813385"
            },
            "pid": {
                "id": 7,
                "name": "Flask",
                "depict": "this is a flask",
                "startValue": "25.00",
                "alertValue": "23.00",
                "min": "0.00",
                "max": "100.00",
                "status": "abnormal",
                "created_time": "2019-06-05T15:50:17.889283"
            },
            "accept_time": "2019-06-10T15:29:57.794671",
            "finish_time": "2019-06-10T15:29:57.794710",
            "is_finished": true
        }
    ],
    "code": 0,
    "total": 3,
    "msg": "返回信息成功"
}
```

#### 8. 根据仪器名称查询维修记录
请求url：` record/inquire/`

请求方式：

请求参数：

- name
- page
- size

返回数据
```
{
    "data": [
        {
            "id": 4,
            "sid": {
                "id": 3,
                "username": "worker2",
                "email": "993626547@qq.com",
                "phone": "13101813385"
            },
            "pid": {
                "id": 7,
                "name": "Flask",
                "depict": "this is a flask",
                "startValue": "25.00",
                "alertValue": "23.00",
                "min": "0.00",
                "max": "100.00",
                "status": "abnormal",
                "created_time": "2019-06-05T15:50:17.889283"
            },
            "accept_time": "2019-06-05T15:50:27.053431",
            "finish_time": "2019-06-05T15:50:27.053490",
            "is_finished": true
        },
        {
            "id": 5,
            "sid": {
                "id": 3,
                "username": "worker2",
                "email": "993626547@qq.com",
                "phone": "13101813385"
            },
            "pid": {
                "id": 7,
                "name": "Flask",
                "depict": "this is a flask",
                "startValue": "25.00",
                "alertValue": "23.00",
                "min": "0.00",
                "max": "100.00",
                "status": "abnormal",
                "created_time": "2019-06-05T15:50:17.889283"
            },
            "accept_time": "2019-06-10T15:29:57.794671",
            "finish_time": "2019-06-10T15:29:57.794710",
            "is_finished": true
        }
    ],
    "code": 0,
    "total": 2,
    "msg": "返回信息成功"
}
```
