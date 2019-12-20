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

def get_userinfo(access_token,openid,lang='zh_CN'):
    #需要用户关注公众号
    query_url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=%s'%(access_token,openid,lang)
    response = requests.get(query_url)
    return json.loads(response.text)

def get_batch_userinfo(access_token,postdata):
    '''postdata ={
    "user_list": [
        {
            "openid": "o-TXmsiCVUNT0iDRRaiW8iTxhx4Q",
            "lang": "zh_CN"
        },
    ]'''
    query_url ='https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token=%s'%access_token
    postdata = json.dumps(postdata,ensure_ascii=False)
    response = requests.post(query_url,postdata)
    return json.loads(response.text)

def get_fans(access_token,next_openid=''):
    #获取关注者列表
    query_url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s'%(access_token,next_openid)
    response = requests.get(query_url)
    return json.loads(response.text)

def create_tag(access_token,name):
    # groups
    create_url = 'https://api.weixin.qq.com/cgi-bin/tags/create?access_token=%s'% access_token
    postData ={  "tag" : { "name" : name  } }
    response = requests.post(create_url,json.dumps(postData,ensure_ascii=False).encode('utf-8'))
    return json.loads(response.text,encoding='utf-8')

def query_tags(access_token):
    query_url ='https://api.weixin.qq.com/cgi-bin/tags/get?access_token=%s'% access_token
    response = requests.get(query_url)
    return json.loads(response.text,encoding='utf-8')

def update_tag(access_token,postData):
    '''{   "tag" : {     "id" : 134,     "name" : "广东人"   } } '''
    update_url='https://api.weixin.qq.com/cgi-bin/tags/update?access_token=%s'% access_token
    postData = json.dumps(postData,ensure_ascii=False).encode('utf-8')
    response = requests.post(update_url, postData)
    return json.loads(response.text,encoding='utf-8')

def delete_tag(access_token,tag_id):
    delete_url ='https://api.weixin.qq.com/cgi-bin/tags/delete?access_token=%s'% access_token
    postData =json.dumps({"tag":{ "id" : tag_id } },ensure_ascii=False).encode('utf-8')
    response = requests.post(delete_url, postData)
    return json.loads(response.text, encoding='utf-8')

def get_tag_fans(access_token,tag_id,next_openid=''):
    #获取标签吓粉丝列表
    query_url ='https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=%s'% access_token
    params ={
        "tagid": tag_id, "next_openid": next_openid
    }
    response = requests.post(query_url,data=params)
    return json.loads(response.text,encoding='utf-8')

def batch_tag(access_token,openids,tag_id):
    tag_url ='https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging?access_token=%s'% access_token
    postData ={
    "openid_list" :openids,
    "tagid" : tag_id
 }
    postData = json.dumps(postData)
    response = requests.post(tag_url, postData)
    return json.loads(response.text, encoding='utf-8')

def batch_untag(accesss_token,openids,tag_id):
    untag_url = 'https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging?access_token=%s' % access_token
    postData = {
        "openid_list": openids,
        "tagid": tag_id
    }
    postData = json.dumps(postData)
    response = requests.post(untag_url, postData)
    return json.loads(response.text, encoding='utf-8')

def query_usertags(access_token,openid):
    query_url='https://api.weixin.qq.com/cgi-bin/tags/getidlist?access_token=%s'% access_token
    postData ={
        'openid':openid
    }
    postData = json.dumps(postData, ensure_ascii=False).encode('utf-8')
    response = requests.post(query_url, postData)
    return json.loads(response.text,encoding='utf-8')

if __name__ == '__main__':
    access_token = wechatBasic.Basic().get_access_token()
    print(access_token)
    postData={   "tag" : {     "id" : 101,     "name" : "测试组"   } }
    #result = create_tag(access_token,'老师')
 #  result = update_tag(access_token,postData)
   # result = get_tag_fans(access_token,103)
  #  result = delete_tag(access_token,102)

  #   result =batch_tag(access_token,['o-TXmsiCVUNT0iDRRaiW8iTxhx4Q'],103)
  # #   result = query_usertags(access_token,'o-TXmsiCVUNT0iDRRaiW8iTxhx4Q')
  #   result = query_usertags(access_token,'o-TXmsiCVUNT0iDRRaiW8iTxhx4Q')
    result = get_fans(access_token)
    print(result)
