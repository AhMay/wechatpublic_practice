#上传下载多媒体文件（临时永久
#https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html
import requests
import json
import os
import wechatBasic

class TempMedia(object):
    '''临时素材'''
    def add_media(self,access_token,media_type,mediafile_path):
        '''

        :param access_token:
        :param media_type: image, voice,video,thumb
        :param mediafile_path:
        :return:
        '''
        add_url = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s'%(access_token,media_type)
        data ={
            'media':open(mediafile_path,'rb')
        }
        response = requests.post(add_url,files=data)
        return json.loads(response.text)

    def get_media(self,access_token,media_id,localpath):
        get_url = 'https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s'%(access_token,media_id)
        response = requests.get(get_url)
        filename = response.headers.get('content-disposition','')
        if filename =='':
            response_text = json.loads(response.text)
            if 'video_url' in response_text.keys():
                video_url = response_text['video_url']
                response = requests.get(video_url)
                filename = os.path.join(localpath,media_id+'.mp4')
        else:
            filename_index = filename.index('filename=')
            filename = filename[filename_index+len('filename='):len(filename)].strip('"')
        with open(os.path.join(localpath,filename),'wb') as fs:
            fs.write(response.content)
        return os.path.join(localpath,filename)

class PermMedia(object):
    def add_media(self,access_token,type,mediafile,video_title='',video_intro=''):
        add_url = 'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s'%(access_token,type)
        postfile ={
            'media': open(mediafile,'rb')
        }
        if type =='video':
            postData={
                'title':video_title,
                'introduction':video_intro
            }
            postData = json.dumps(postData,ensure_ascii=False)
            postfile['description'] =postData

        response = requests.post(add_url, files=postfile)
        return json.loads(response.text)

    def add_news(self,access_token,articles):
        '''{
    "articles": [{
     "title": TITLE,
    "thumb_media_id": THUMB_MEDIA_ID, #必须是永久图文消息
    "author": AUTHOR,
    "digest": DIGEST,
    "show_cover_pic": SHOW_COVER_PIC(0 / 1),
    "content": CONTENT, #图文消息的具体内容，支持HTML标签。必须少于2万字符.涉及图片url必须来源'上传图文消息内的图片获取url'接口获取
    "content_source_url": CONTENT_SOURCE_URL,
    "need_open_comment":1,
    "only_fans_can_comment":1
},
    //若新增的是多图文素材，则此处应还有几段articles结构
]
}'''
        add_url = 'https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=%s'% access_token
        postData = {
            'articles':articles
        }
        postData = json.dumps(postData,ensure_ascii=False).encode('utf-8')
        response = requests.post(add_url,postData)
        return json.loads(response.text)

    def upload_newsurl(self,access_token,picfile):
        upload_url = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=%s'% access_token
        postData ={
            'media':open(picfile,'rb')
        }
        response = requests.post(upload_url,files=postData)
        return json.loads(response)['url']

    def get_media(self,access_token,media_id):
        get_url = 'https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s'% access_token
        postData ={
            'media':media_id
        }
        response = requests.post(get_url,json.dumps(postData))
        return json.loads(response.text,encoding='utf-8')

if __name__ == '__main__':
    access_token = wechatBasic.Basic().get_access_token()
    perm_media = PermMedia()
    result=perm_media.add_media(access_token,'image',r'E:\MayWorld\May收集的图片\qrcode.jpg')
    result = perm_media.get_media(access_token,result['media_id'])
    print(result)