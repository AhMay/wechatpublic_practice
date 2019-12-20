from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .wechatCallbackapiTest import *
from .wechatOAuthTest import *

# Create your views here.

def index(request):
    userinfo={}
    if request.GET.get('code','') is not '':
        code = request.GET.get('code')
        print('Oauth2.0')
        print(code)
        oauthTest = wechatOAuthTest()
        userinfo = oauthTest.getUserInfo(code)
        print(userinfo)
        return render(request,'app/userinfo.html',{'userinfo':userinfo})
    return render(request,'app/userinfo.html',{'userinfo':userinfo})

@csrf_exempt
def wechatindex(request):
    wechatObj = wechatCallbackapiTest(request)
    if request.GET.get('echostr',None):
        echostr = wechatObj.valid()
        return HttpResponse(echostr)
    else:
        #POST
        #result = wechatObj.responseMsg()
        result = wechatObj.selfAnswer()
        return HttpResponse(result)