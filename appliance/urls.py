from django.urls import path
from . import views

app_name='product'


# appliance路由设计
urlpatterns = [
    path('appliance/all/', views.ApplianceList.as_view()),
    path('appliance/add/',views.ApplianceList.as_view()),
    path('appliance/inquire/', views.ApplianceSearch.as_view()),
    path('appliance/update/', views.ApplianceUpdate.as_view()),
    path('appliance/delete/', views.ApplianceDelete.as_view()),
    path('appliance/data/', views.ApplianceData.as_view()),
    path('record/',views.RepaircordView.as_view()),
    path('record/inquire/',views.RepairSearch.as_view()),
    path('handle/', views.HandleView.as_view())
]