'''微信公众号接收到的用户消息类型
https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html
'''
import time

class ReceiveMsg(object):
    '''基类'''
    def __init__(self,xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

class ReceiveTextMsg(ReceiveMsg):
    '''文本消息'''
    def __init__(self,xmlData):
        super(ReceiveTextMsg,self).__init__(xmlData)
        self.content = xmlData.find('Content').text.encode('utf-8')

class ReceiveImageMsg(ReceiveMsg):
    '''图片消息'''
    def __init__(self,xmlData):
        super(ReceiveImageMsg,self).__init__(xmlData)
        self.PicUrl = xmlData.find('PicUrl').text.encode('utf-8')
        self.MediaId = xmlData.find('MediaId').text

class ReceiveVoiceMsg(ReceiveMsg):
    '''语音消息'''
    def __init__(self,xmlData):
        super(ReceiveVoiceMsg,self).__init__(xmlData)
        self.Format = xmlData.find('Format').text
        self.MediaId = xmlData.find('MediaId').text
        self.Recognition = ''
        if xmlData.find('Recognition') is not None:
            self.Recognition = xmlData.find('Recognition').text

class ReceiveVideoMsg(ReceiveMsg):
    '''视频消息和小视频消息'''
    def __init__(self,xmlData):
        super(ReceiveVideoMsg,self).__init__(xmlData)
        self.ThumbMediaId = xmlData.find('ThumbMediaId').text
        self.MediaId = xmlData.find('MediaId').text

class ReceiveLocationMsg(ReceiveMsg):
    '''地理位置消息'''
    def __init__(self,xmlData):
        super(ReceiveLocationMsg,self).__init__(xmlData)
        self.Location_X = xmlData.find('Location_X').text
        self.Location_Y = xmlData.find('Location_Y').text
        self.Scale = xmlData.find('Scale').text
        self.Label = xmlData.find('Label').text.encode('utf-8')

class ReceiveLinkMsg(ReceiveMsg):
    '''链接消息'''
    def __init__(self,xmlData):
        super(ReceiveLinkMsg,self).__init__(xmlData)
        self.Title = xmlData.find('Title').text.encode('utf-8')
        self.Description = xmlData.find('Description').text.encode('utf-8')
        self.Url = xmlData.find('Url').text