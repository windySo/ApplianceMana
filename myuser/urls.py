from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name='myuser'

urlpatterns = [

    path('user/all/', views.UserList.as_view()),
    path('user/inquire/', views.UserSearch.as_view()),
    path('user/delete/',views.UserDelete.as_view()),
    path('user/change/', views.InfoChange.as_view()),
    path('sign/register/',views.RegisterView2.as_view()),
    path('sign/login/', obtain_jwt_token),
    path('public/email/',views.CodeSend.as_view()),

]