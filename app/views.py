from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .wechatCallbackapiTest import *

# Create your views here.

def index(request):
    return HttpResponse('normal page')

@csrf_exempt
def wechatindex(request):
    print('here')
    wechatObj = wechatCallbackapiTest(request)
    if request.GET.get('echostr',None):
        echostr = wechatObj.valid()
        return HttpResponse(echostr)
    else:
        #POST
        result = wechatObj.responseMsg()
        return HttpResponse(result)