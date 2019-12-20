'''
生成带参数二维码
https://developers.weixin.qq.com/doc/offiaccount/Account_Management/Generating_a_Parametric_QR_Code.html
'''
import requests
import json
import urllib.parse
import wechatBasic
from wechat_Const import *

def create_ticket(access_token,action_name='QR_SCENE',scene=1,expire_seconds=1800):
    postData ={'action_name': action_name}
    if type(scene) == str:
        postData['action_info'] ={'scene':{
            'scene_str':scene
        }}
    elif type(scene) == int:
        postData['action_info'] = {'scene': {
            'scene_id': scene
        }}
    else:
        raise ValueError('scene type must be str or int')
    if action_name == 'QR_SCENE':
        print('创建临时二维码ticket')
        postData['expire_seconds']=expire_seconds

    ticket_create_url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s'% access_token
    response = requests.post(ticket_create_url,json.dumps(postData))
    return json.loads(response.text)

def exchange_qrcode(ticket):
    exchange_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode'
    params = {
        'ticket':ticket
    }
    response = requests.get(exchange_url,params=params)
    with open('test.jpg','wb') as qrimg:
        qrimg.write(response.content)
    return response.headers

def convert_shorturl(access_token,ticket):
    params =urllib.parse.urlencode({
        'ticket': ticket
    })
    exchange_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?%s' % params
    convert_url = 'https://api.weixin.qq.com/cgi-bin/shorturl?access_token=%s'%access_token
    convert_data={
     'action':'long2short',
     'long_url':exchange_url
    }
    response = requests.post(convert_url,json.dumps(convert_data))
    short_url = json.loads(response.text)['short_url']
    qr_response = requests.get(short_url)
    with open('qrcode.jpg', 'wb') as qrimg:
        qrimg.write(qr_response.content)
    return short_url

if __name__ == '__main__':
    access_token = wechatBasic.Basic().get_access_token()
    result = create_ticket(access_token)
    print(result)
    result = convert_shorturl(access_token,result['ticket'])
    print(result)
