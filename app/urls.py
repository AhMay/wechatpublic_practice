from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('',index, name='index'),
    path('wechat/', wechatindex, name='wechat'),
]