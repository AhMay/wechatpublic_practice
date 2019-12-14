'''微信公众号回复用户消息类型
https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Passive_user_reply_message.html
'''
import time

class ReplyMsg(object):
    '''基类'''
    def __init__(self,toUser,fromUser):
        self.toUser = toUser
        self.fromUser = fromUser

    def send(self):
        return 'success'

class ReplyTextMsg(ReplyMsg):
    '''文本消息'''
    def __init__(self, toUser, fromUser,content):
        super(ReplyTextMsg,self).__init__(toUser,fromUser)
        self.content = content

    def send(self):
        xmlForm = '''
            <xml>
  <ToUserName><![CDATA[{0}]]></ToUserName>
  <FromUserName><![CDATA[{1}]]></FromUserName>
  <CreateTime>{2}</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[{3}]]></Content>
</xml>
        '''

        return xmlForm.format(self.toUser,self.fromUser,str(int(time.time())),self.content)


class ReplyImageMsg(ReplyMsg):
    '''图片消息'''
    def __init__(self, toUser, fromUser, media_id):
        super(ReplyImageMsg, self).__init__(toUser, fromUser)
        self.media_id = media_id

    def send(self):
        xmlForm = '''
           <xml>
  <ToUserName><![CDATA[{0}]]></ToUserName>
  <FromUserName><![CDATA[{1}]]></FromUserName>
  <CreateTime>{2}</CreateTime>
  <MsgType><![CDATA[image]]></MsgType>
  <Image>
    <MediaId><![CDATA[{3}]]></MediaId>
  </Image>
</xml>
        '''

        return xmlForm.format(self.toUser, self.fromUser, str(int(time.time())), self.media_id)

class ReplyVoiceMsg(ReplyMsg):
    '''语音消息'''
    def __init__(self, toUser, fromUser, media_id):
        super(ReplyVoiceMsg, self).__init__(toUser, fromUser)
        self.media_id = media_id

    def send(self):
        xmlForm = '''
           <xml>
  <ToUserName><![CDATA[{0}]]></ToUserName>
  <FromUserName><![CDATA[{1}]]></FromUserName>
  <CreateTime>{2}</CreateTime>
  <MsgType><![CDATA[voice]]></MsgType>
  <Voice>
    <MediaId><![CDATA[{3}]]></MediaId>
  </Voice
</xml>
        '''

        return xmlForm.format(self.toUser, self.fromUser, str(int(time.time())), self.media_id)

class ReplyVideoMsg(ReplyMsg):
    '''视频消息'''
    def __init__(self, toUser, fromUser, media_id,thumbmedia_id,title='',description=''):
        super(ReplyVideoMsg, self).__init__(toUser, fromUser)
        self.media_id = media_id
        self.thumbmedia_id = thumbmedia_id
        self.title = title
        self.description = description

    def send(self):
        xmlForm = '''
        <xml>
  <ToUserName><![CDATA[{0}]]></ToUserName>
  <FromUserName><![CDATA[{1}]]></FromUserName>
  <CreateTime>{2}</CreateTime>
  <MsgType><![CDATA[video]]></MsgType>
  <Video>
    <MediaId><![CDATA[{3}]]></MediaId>
    <ThumbMediaId><![CDATA[{4}]]></ThumbMediaId>
    <Title><![CDATA[{5}]]></Title>
    <Description><![CDATA[{6}]]></Description>
  </Video>
</xml>
        '''
        return xmlForm.format(self.toUser, self.fromUser, str(int(time.time())), self.media_id,
                              self.thumbmedia_id,self.title,self.description)

class ReplyNewsMsg(ReplyMsg):
    '''图文消息'''
    def __init__(self, toUser, fromUser, newsitems):
        super(ReplyNewsMsg, self).__init__(toUser, fromUser)
        self.newsitems = newsitems

    def send(self):
        xmlForm = '''
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
        itemXml = NewsItem.itemsXml(self.newsitems)
        return xmlForm.format(self.toUser, self.fromUser, str(int(time.time())), len(self.newsitems),
                              itemXml)

class NewsItem(object):
    '''图文item'''
    def __init__(self,title,description,picurl,url):
        self.title = title
        self.description = description
        self.picurl = picurl
        self.url = url

    def __itemXml(self):
        xmlItem = '''
            <item>
      <Title><![CDATA[{0}]]></Title>
      <Description><![CDATA[{1}]]></Description>
      <PicUrl><![CDATA[{2}]]></PicUrl>
      <Url><![CDATA[{3}]]></Url>
    </item>
        '''
        return xmlItem.format(self.title,self.description,self.picurl,self.url)

    @classmethod
    def itemsXml(cls,newsItemobjs):
        '''多图文时需要'''
        xmlstr =''
        if not isinstance(newsItemobjs,list):
            raise Exception('请将NewsItem的对象存到数组中')
        for item in newsItemobjs:
            if not isinstance(item,NewsItem):
                raise  Exception('所有的元素必须时NewsItem对象')
            xmlstr += item.__itemXml()

        return xmlstr
