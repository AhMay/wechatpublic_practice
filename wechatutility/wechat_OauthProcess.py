import requests
import json

from wechatutility.wechat_Const import *

def exchange_access_token(code):
    exchange_url = ' https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(
        appId,appSecret,code
    )
    response = requests.get(exchange_url)
    return json.loads(response.text)

def refresh_access_token(refresh_token):
    refresh_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={0}&grant_type=refresh_token&refresh_token={1}'.format(
        appId,refresh_token
    )
    response = requests.get(refresh_url)
    return json.loads(response.text)

def query_userinfo(access_token,openid,lang='zh_CN'):
    #无需关注
    query_url='https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang={2}'.format(
        access_token,openid,lang
    )
    response = requests.get(query_url)
    return json.loads(response.content)

def very_access_token_valid(access_token,openid):
    very_url = 'https://api.weixin.qq.com/sns/auth?access_token={0}&openid={1}'.format(access_token,openid)
    response = requests.get(very_url)
    result = json.loads(response.text)
    if result['errcode'] == 0:
        return True
    else:
        return False

if __name__ == '__main__':
    result = exchange_access_token('081574Gt1SWI4f0rkrFt1qrlGt1574Gt')
    print(result)
    print(very_access_token_valid(result['access_token'],result['openid']))
    #userinfo = query_userinfo(result['access_token'],result['openid'])
  #  result = refresh_access_token('28_a3YKiuKaeQhx5rGx9jCYn6NyrFycQwBgq25ofsIiqYWf0lcn2VL3uNqK6LgKBLwEgZiNGCKrAATn5QqDgAzVBP9-pwn9nheMRXogEe_jxrM')

    #print(userinfo)