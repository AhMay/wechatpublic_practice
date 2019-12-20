#客服接口
#https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html
import requests
import json
import wechatBasic

def add_kfaccount(access_token, json_data):
    '''
    {
     "kf_account" : "test1@test",
     "nickname" : "客服1",
     "password" : "pswmd5"
}
    :param access_token:
    :param json_data:
    :return:
    '''
    kfaccount_add_url = 'https://api.weixin.qq.com/customservice/kfaccount/add?access_token=%s'% access_token
    json_data = json.dumps(json_data,ensure_ascii=False)
    response = requests.post(kfaccount_add_url,json_data.encode('utf-8'))
    return json.loads(response.text)

def update_kfaccount(access_token, json_data):
    kfaccount_update_url = 'https://api.weixin.qq.com/customservice/kfaccount/update?access_token=%s'% access_token
    json_data = json.dumps(json_data,ensure_ascii=False)
    response = requests.post(kfaccount_update_url,json_data.encode('utf-8'))
    return json.loads(response.text)

def delete_kfaccount(access_token, json_data):
    kfaccount_delete_url = 'https://api.weixin.qq.com/customservice/kfaccount/del?access_token=%s'% access_token
    json_data = json.dumps(json_data,ensure_ascii=False)
    #官方文档说是GET，但感觉是官方文档错误。
    response = requests.post(kfaccount_delete_url,json_data.encode('utf-8'))
    return json.loads(response.text)

def set_kfaccount_headingimg(access_token,kfaccount,img_path):
    '''

    :param access_token:
    :param kfaccount: test1@test1
    :param img_path:
    :return:
    '''
    uploading_url = 'http://api.weixin.qq.com/customservice/kfaccount/uploadheadimg?access_token=%s&kf_account=%s'%\
                    (access_token,kfaccount)
    data ={
        'media':open(img_path,'rb')
    }
    response = requests.post(uploading_url,files=data)
    return json.loads(response.text)

def query_kfaccounts(access_token):
    query_url = 'https://api.weixin.qq.com/cgi-bin/customservice/getkflist?access_token=%s'% access_token
    response = requests.get(query_url)
    return json.loads(response.content)

def send_kfmsg(access_token,json_data):
    send_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s'% access_token
    json_data = json.dumps(json_data,ensure_ascii=False)
    response = requests.post(send_url, json_data.encode('utf-8'))

    return json.loads(response.text)

def send_kfstatus(access_token, input_type):
    '''{ "touser":"OPENID", "command":"Typing"}'''
    if input_type not in ('Typing','CancelTyping'):
        raise Exception('输入状态必须是：' + 'Typing' + '或者:' + 'CancelTyping')
    send_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/typing?access_token=%s'% access_token
    json_data = json.dumps(input_type)
    response = requests.post(send_url, json_data)
    return json.loads(response.text)

if __name__ == '__main__':
    access_token = wechatBasic.Basic().get_access_token()
    kfaccount = {
     "kf_account" : "test1@test",
     "nickname" : "客服1",
     "password" : "pswmd5"
}
    result = query_kfaccounts(access_token)
    print(result)