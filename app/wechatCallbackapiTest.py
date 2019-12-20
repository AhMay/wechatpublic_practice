import hashlib
import time
import xml.etree.ElementTree as ET
import requests
import json
from wechatutility.WXBizMsgCrypt import WXBizMsgCrypt
from wechatutility.wechatReceiveMsg import *
from wechatutility.wechatReplyMsg import *


TOKEN = 'wechatpublic'
#消息体加密模式
APPID = 'wx4409cf14b491bef5'
EncodingAESKey = 'fhkHwM6bIhSUIEjWQVDUHcWeei8xpimi01dICJq9Lkb'

class wechatCallbackapiTest():
    def __init__(self,request):
        self.request = request

    def valid(self):
        echoStr = self.request.GET['echostr']
        if self._checkSignature():
            return echoStr  # 验证成功的话，要返回 echoStr到微信公众平台
        else:
            return ''

    def selfAnswer(self):
        encrypt_type = self.request.GET.get('encrypt_type', None)
        pc, postStr = self._encrypt_data(encrypt_type)
        recMsg = parse_xml(postStr)
        if recMsg is None:
            return 'success'
        elif isinstance(recMsg,ReceiveTextMsg):
            #测试 Oauth认证
            content = '<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx349372b8988f6776&redirect_uri=http://ahmay.ngrok2.xiaomiqiu.cn/&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect">' \
                      '单击这里体验OAuth授权</a>'
           # replyMsg = ReplyTextMsg(recMsg.FromUserName,recMsg.ToUserName,recMsg.Content)
            replyMsg = ReplyTextMsg(recMsg.FromUserName, recMsg.ToUserName, content)
        elif isinstance(recMsg,ReceiveImageMsg):
            replyMsg = ReplyImageMsg(recMsg.FromUserName, recMsg.ToUserName, recMsg.MediaId)
        elif isinstance(recMsg,ReceiveVoiceMsg):
            print(postStr)
            if recMsg.Recognition is not '':
                content = '你说的是：' + recMsg.Recognition
                replyMsg = ReplyTextMsg(recMsg.FromUserName, recMsg.ToUserName, content)
            else:
                replyMsg = ReplyVoiceMsg(recMsg.FromUserName, recMsg.ToUserName, recMsg.MediaId)

        elif isinstance(recMsg,ReceiveVideoMsg):
            replyMsg = ReplyVideoMsg(recMsg.FromUserName, recMsg.ToUserName, recMsg.MediaId,recMsg.ThumbMediaId)
        elif isinstance(recMsg,ReceiveLocationMsg):
            content = '你发送的是位置，\n纬度为：' + recMsg.Location_X+ ';\n经度为: ' + recMsg.Location_Y \
                      + ';\n缩放级别为: ' + recMsg.Scale + '; \n位置为: ' + recMsg.Label
            replyMsg = ReplyTextMsg(recMsg.FromUserName, recMsg.ToUserName, content)
        elif isinstance(recMsg,ReceiveLinkMsg):
            content = '你发送的是链接，标题为 ：' + recMsg.Title + '; 内容为：' + recMsg.Description + \
            '; 链接地址为：' + recMsg.Url
            replyMsg = ReplyTextMsg(recMsg.FromUserName,recMsg.ToUserName,content)
        elif isinstance(recMsg,ReceiveEventMsg):
            print(postStr)
            print('event here')
            content = '有事件发生 Event：' + recMsg.Event +'\n'
            content += 'EventKey: ' + recMsg.EventKey[1] if recMsg.EventKey[0] is True else '' +'\n\n'
            content += 'Ticket: ' + recMsg.Ticket[1] if recMsg.Ticket[0] is True else '' +'\n'
            if isinstance(recMsg,ReveiveLocationEventMsg):
                content += '纬度: ' + recMsg.Latitude +'\n'
                content += '经度: ' + recMsg.Longitude + '\n'
                content += '精确度: ' + recMsg.Precision + '\n'
                ak = 'QGeUGqrqWwHNSMWC0QOHixE4DGvH7AH0'
                url = 'http://api.map.baidu.com/geocoder?location={0},{1}&output=json&key={2}'.format(
                    recMsg.Latitude,recMsg.Longitude,ak
                )
                response = requests.get(url)

            replyMsg = ReplyTextMsg(recMsg.FromUserName,recMsg.ToUserName,response.text)

        return replyMsg.send()

    def responseMsg(self):
        encrypt_type = self.request.GET.get('encrypt_type', None)
        pc, postStr = self._encrypt_data(encrypt_type)
        postObj = self._parseMsg(postStr)
        print(postObj)
        msg_type = postObj['MsgType']
        result = ''
        if msg_type == 'text':
            result = self._receiveText(postObj)
        elif msg_type == 'image':
            result = self._receiveImage(postObj)
        elif msg_type == 'voice':
            result = self._receiveVoice(postObj)
        elif msg_type == 'video' or msg_type == 'shortvideo':
            print('视频')
            print(msg_type)
            result = self._receiveVideo(postObj)
        elif msg_type == 'location':
            result = self._receiveLocation(postObj)
        elif msg_type == 'link':
            result = self._receiveLink(postObj)
        elif msg_type == 'event':
            result = self._receiveEvent(postObj)
        else:
            result = '不能识别的 msg type: ' + msg_type
            print(result)

        if encrypt_type is not None and encrypt_type == 'aes':  # 解密
            nonce = self.request.GET['nonce']
            ret, encryotMsg = pc.EncryptMsg(result, nonce, str(int(time.time())))
            result = encryotMsg
        return result

    def _encrypt_data(self,encrypt_type):
        pc = None
        if encrypt_type is not None and encrypt_type == 'aes':  # 解密
            timestamp = self.request.GET['timestamp']
            nonce = self.request.GET['nonce']
            msg_signature = self.request.GET['msg_signature']
            pc = WXBizMsgCrypt(TOKEN, EncodingAESKey, APPID)
            ret, descryptMsg = pc.DecryptMsg(self.request.body, msg_signature, timestamp, nonce)
            if ret != 0:
                print(ret)
                return ''
            postStr = descryptMsg
        else:
            postStr = self.request.body

        return  pc, postStr

    def _checkSignature(self):
        signature = self.request.GET['signature']
        timestamp = self.request.GET['timestamp']
        nonce = self.request.GET['nonce']
        list = [TOKEN,timestamp,nonce]
        list.sort()
        sha1 = hashlib.sha1()
        sha1.update(list[0].encode('utf-8'))
        sha1.update(list[1].encode('utf-8'))
        sha1.update(list[2].encode('utf-8'))
        hashcode = sha1.hexdigest()
        print('hashcode:' + hashcode)
        print('signature:' + signature)
        if hashcode == signature:
            return True
        else:
            return False

    def _parseMsg(self,xmlbody):
        '''解析用户发送的消息'''
        try:
            xmlData = ET.fromstring(xmlbody)
            msg ={}
            msg['ToUserName'] = xmlData.find('ToUserName').text
            msg['FromUserName'] = xmlData.find('FromUserName').text
            msg['CreateTime'] = xmlData.find('CreateTime').text
            msg['MsgType'] = xmlData.find('MsgType').text
            msg['MsgId'] = xmlData.find('MsgId').text
            if msg['MsgType']  == 'text':
                msg['Content'] = xmlData.find('Content').text
            elif msg['MsgType']  == 'image':
                msg['PicUrl'] = xmlData.find('PicUrl').text
                msg['MediaId'] = xmlData.find('MediaId').text
            elif msg['MsgType']  == 'voice':
                msg['MediaId'] = xmlData.find('MediaId').text
                msg['Format'] = xmlData.find('Format').text
                msg['Recognition'] = xmlData.find('Recognition').text
            elif msg['MsgType']  == 'video':
                msg['MediaId'] = xmlData.find('MediaId').text
                msg['ThumbMediaId'] = xmlData.find('ThumbMediaId').text
            elif msg['MsgType']  == 'location':
                msg['Location_X'] = xmlData.find('Location_X').text  # 地理位置消息
                msg['Location_Y'] = xmlData.find('Location_Y').text
                msg['Scale'] = xmlData.find('Scale').text
                msg['Label'] = xmlData.find('Label').text
            elif msg['MsgType']  == 'link':
                msg['Title'] = xmlData.find('Title').text
                msg['Description'] = xmlData.find('Description').text
                msg['Url'] = xmlData.find('Url').text
            return msg
        except Exception as e:
            raise  e

    def _receiveText(self,obj):
        keyword = obj['Content']
        if keyword == '文本':
            content = '这是一个文本消息'
        elif keyword == '单图文':
            content = list()
            content.append({
                'Title':'单图文标题',
                'Description':'单图文消息内容',
                'PicUrl':'https://img.zcool.cn/community/0150aa5c0a32bca80121ab5d8175af.png@1280w_1l_2o_100sh.png',
                'Url':'https://www.toutiao.com/a6769481430914302478/'
            })
        elif keyword == '图文' or keyword == '多图文':
            content = list()
            content.append({
                'Title': '多图文标题2',
                'Description': '标题2图文消息内容',
                'PicUrl': 'http://mpic.haiwainet.cn/thumb/d/uploadfile/20191213/1576191869519087,w_480.jpg',
                'Url': 'https://m.haiwainet.cn/ttc/3541093/2019/1213/content_31681194_1.html?tt_group_id=6769695517677978123'
            })
            content.append({
                'Title':'多图文标题1',
                'Description':'标题1图文消息内容',
                'PicUrl':'https://img.zcool.cn/community/0150aa5c0a32bca80121ab5d8175af.png@1280w_1l_2o_100sh.png',
                'Url':'https://www.toutiao.com/a6769481430914302478/'
            })

            content.append({
                'Title': '多图文标题3',
                'Description': '标题3图文消息内容',
                'PicUrl': 'http://p3.pstatp.com/large/pgc-image/bf912a558ef743e293d054339eff40d5',
                'Url': 'https://www.toutiao.com/a6769534922555130371/'
            })
        elif keyword == '音乐':
            content = list()
            content.append({
                'Title':'最炫民族风',
                'Description':'歌手：凤凰传奇',
                'MusicUrl':'https://music.163.com/#/song?id=29418062',
                'HQMusicUrl':'https://music.163.com/#/song?id=28757351',
               # 'ThumbMediaId':1
            })
        else:
            content = '你发送的是一个文本，内容为' + keyword + '\n\n'
            content += time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) +'\n' + obj['FromUserName'] + '\n 技术支持 AhMay'

        if isinstance(content,list):
            item0 = content[0]
            if 'MusicUrl' in item0.keys():
                return self._transmitMusic(obj,item0)
            else:
                return self._transmitNews(obj,content)
        else:
            return self._transmitText(obj,content)

    def _receiveImage(self,obj):
        content = '你发送的是图片，地址为：' + obj['PicUrl']
        result = self._transmitText(obj,content)
        return result

    def _receiveVoice(self,obj):
        content = '你发送的是语音，媒体ID为：' + obj['MediaId']
        result = self._transmitText(obj,content)
        return result

    def _receiveVideo(self,obj):
        content = '你发送的是视频，媒体ID为：' + obj['MediaId']
        result = self._transmitText(obj,content)
        return result

    def _receiveLocation(self,obj):
        content = '你发送的是位置，\n纬度为：' + obj['Location_X'] +';\n经度为: ' + obj['Location_Y'] \
            + ';\n缩放级别为: ' + obj['Scale'] + '; \n位置为: ' + obj['Label']
        result = self._transmitText(obj,content)
        return result

    def _receiveLink(self,obj):
        content = '你发送的是链接，标题为 ：' + obj['Title'] + '; 内容为：' + obj['Description'] + \
            '; 链接地址为：' + obj['Url']
        result = self._transmitText(obj,content)
        return result

    def _receiveEvent(self, obj):
        content = ''
        if obj['Event'] == 'subscribe':
            content = '欢迎关注AhMay的公众号'

        result = self._transmitText(obj, content)
        return result

    def _transmitText(self,obj,content):
        xmlTpl ='''
        <xml>
  <ToUserName><![CDATA[{0}]]></ToUserName>
  <FromUserName><![CDATA[{1}]]></FromUserName>
  <CreateTime>{2}</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[{3}]]></Content>
</xml>
        '''
        result = xmlTpl.format(obj['FromUserName'],obj['ToUserName'],int(time.time()),content)
        return result

    def _transmitNews(self, obj, newsArray):
        xmlItem = '''
         <item>
      <Title><![CDATA[{0}]]></Title>
      <Description><![CDATA[{1}]]></Description>
      <PicUrl><![CDATA[{2}]]></PicUrl>
      <Url><![CDATA[{3}]]></Url>
    </item>
        '''
        newsItems = []
        for news in newsArray:
            news = xmlItem.format(news['Title'],news['Description'],news['PicUrl'],news['Url'])
            newsItems.append(news)
        itemstr = ''.join(newsItems)
        xmlTpl = '''
           <xml>
  <ToUserName><![CDATA[{0}]]></ToUserName>
  <FromUserName><![CDATA[{1}]]></FromUserName>
  <CreateTime>{2}</CreateTime>
  <MsgType><![CDATA[news]]></MsgType>
  <ArticleCount>{3}</ArticleCount>
  <Articles>
    {4}
  </Articles>
</xml>
            '''
        result = xmlTpl.format(obj['FromUserName'], obj['ToUserName'], str(int(time.time())), len(newsItems),itemstr)
        return result

    def _transmitMusic(self, obj, musicArray):

        xmlTpl = '''
           <xml>
  <ToUserName><![CDATA[{0}]]></ToUserName>
  <FromUserName><![CDATA[{1}]]></FromUserName>
  <CreateTime>{2}</CreateTime>
  <MsgType><![CDATA[music]]></MsgType>
  <Music>
    <Title><![CDATA[{3}]]></Title>
    <Description><![CDATA[{4}]]></Description>
    <MusicUrl><![CDATA[{5}]]></MusicUrl>
    <HQMusicUrl><![CDATA[{6}]]></HQMusicUrl>
   
  </Music>
</xml>
            '''
        result = xmlTpl.format(obj['FromUserName'], obj['ToUserName'], str(int(time.time())),
                               musicArray['Title'],
                               musicArray['Description'],
                               musicArray['MusicUrl'],
                               musicArray['HQMusicUrl'],
                            #   str(musicArray['ThumbMediaId']),
                               )
        print(result)
        return result


