#群发消息管理
#https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Batch_Sends_and_Originality_Checks.html
import requests
import json
import wechatBasic
import wechat_mediafileManage

def send_massmsg(access_token,postData):
    send_url ='https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=%s'% access_token
    response = requests.post(send_url,json.dumps(postData))
    return json.loads(response.text)

def del_massmsg(access_token,msg_id, article_idx=0):
    '''只能删除图文和视频消息.收到消息的用户点击时会显示已被删除'''
    del_url = 'https://api.weixin.qq.com/cgi-bin/message/mass/delete?access_token=%s'% access_token
    postData={
        "msg_id": msg_id,
        "article_idx": article_idx
    }
    response = requests.post(del_url, json.dumps(postData))
    return json.loads(response.text)

def preview_massmsg(access_token,postData):
    '''预览接口'''
    send_url = 'https://api.weixin.qq.com/cgi-bin/message/mass/preview?access_token=%s' % access_token
    response = requests.post(send_url, json.dumps(postData))
    return json.loads(response.text)

def get_massmsg_status(access_token,msg_id):
    '''查看消息状态'''
    send_url = 'https://api.weixin.qq.com/cgi-bin/message/mass/get?access_token=%s' % access_token
    postData = {
   "msg_id": msg_id
}
    response = requests.post(send_url, json.dumps(postData))
    return json.loads(response.text)

def get_massend_speed(access_token):
    speed_url ='https://api.weixin.qq.com/cgi-bin/message/mass/speed/get?access_token=%s'% access_token
    response = requests.get(speed_url, json.dumps(postData))
    return json.loads(response.text)

def set_massend_speed(access_token,speed):
    speed_url = 'https://api.weixin.qq.com/cgi-bin/message/mass/speed/set?access_token=%s'%access_token
    postData = {
        'speed':speed
    }
    response = requests.post(speed_url, json.dumps(postData))
    return json.loads(response.text)

def upload_news(access_token,articles):
    ''' {
                        "thumb_media_id":"qI6_Ze_6PtV7svjolgs-rN6stStuHIjs9_DidOHaj0Q-mwvBelOXCFZiq2OsIU-p",
                        "author":"xxx",
                        "title":"Happy Day",
                        "content_source_url":"www.qq.com",
                        "content":"content",
                        "digest":"digest",
                        "show_cover_pic":1,
                        "need_open_comment":1,
                        "only_fans_can_comment":1
                        },'''
    upload_url ='https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token=%s'% access_token
    postData = {
        'articles':articles
    }
    postData = json.dumps(postData,ensure_ascii=False).encode('utf-8')
    response = requests.post(upload_url,postData)

    return json.loads(response.text,encoding='utf-8')


if __name__ == '__main__':
    access_token = wechatBasic.Basic().get_access_token()
    articles =[
        {
            "thumb_media_id": "uKTr5qdP5-mMPBddXE87C8Mml1vWCZqt0H4aAv-HNvzLVlaHn54_P99t4qjATizv",
            "author": "xxx",
            "title": "Happy Day",
            "content_source_url": "www.qq.com",
            "content": "content",
            "digest": "digest",
            "show_cover_pic": 1,
            "need_open_comment": 1,
            "only_fans_can_comment": 1
        }
    ]

    #result = upload_news(access_token,articles)
    postData={
        "filter": {
            "is_to_all": False,
            "tag_id": 2
        },
        "image": {
            "media_id": "uKTr5qdP5-mMPBddXE87C8Mml1vWCZqt0H4aAv-HNvzLVlaHn54_P99t4qjATizv"
        },
        "msgtype": "image"
    }
    result = send_massmsg(access_token,postData)
    print(result)