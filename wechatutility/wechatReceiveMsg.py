'''微信公众号接收到的用户消息类型
https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html
'''

import xml.etree.ElementTree as ET

def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return ReceiveTextMsg(xmlData)
    elif msg_type == 'image':
        return ReceiveImageMsg(xmlData)
    elif msg_type == 'voice':
        return ReceiveVoiceMsg(xmlData)
    elif msg_type in ('video','shortvideo'):
        return ReceiveVideoMsg(xmlData)
    elif msg_type == 'location':
        return ReceiveLocationMsg(xmlData)
    elif msg_type == 'link':
        return ReceiveLinkMsg(xmlData)
    elif msg_type == 'event':
        recEventObj = ReceiveEventMsg(xmlData)
        if recEventObj.Event == 'LOCATION':
            return ReveiveLocationEventMsg(xmlData)
        return recEventObj
    else:
        print('不能识别的消息类型:'+ msg_type)
        return None

class ReceiveMsg(object):
    '''基类'''
    def __init__(self,xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId =''
        if xmlData.find('MsgId') is not None:
             self.MsgId = xmlData.find('MsgId').text

class ReceiveTextMsg(ReceiveMsg):
    '''文本消息'''
    def __init__(self,xmlData):
        super(ReceiveTextMsg,self).__init__(xmlData)
        self.Content = xmlData.find('Content').text

class ReceiveImageMsg(ReceiveMsg):
    '''图片消息'''
    def __init__(self,xmlData):
        super(ReceiveImageMsg,self).__init__(xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
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
        self.Label = xmlData.find('Label').text

class ReceiveLinkMsg(ReceiveMsg):
    '''链接消息'''
    def __init__(self,xmlData):
        super(ReceiveLinkMsg,self).__init__(xmlData)
        self.Title = xmlData.find('Title').text
        self.Description = xmlData.find('Description').text
        self.Url = xmlData.find('Url').text

class ReceiveEventMsg(ReceiveMsg):
    '''普通事件'''
    def __init__(self, xmlData):
        super(ReceiveEventMsg,self).__init__(xmlData)
        self.Event = xmlData.find('Event').text
        self.EventKey = (False,'')
        if xmlData.find('EventKey') is not None:
            eventkey ='' if xmlData.find('EventKey').text is None else xmlData.find('EventKey').text
            self.EventKey =(True, eventkey)

        self.Ticket = (False,'')
        if xmlData.find('Ticket') is not None:
            ticket = '' if xmlData.find('Ticket').text is None else xmlData.find('Ticket').text
            self.EventKey =(True, ticket)

class ReveiveLocationEventMsg(ReceiveEventMsg):
    '''上报地理位置事件'''
    def __init__(self,xmlData):
        super(ReveiveLocationEventMsg,self).__init__(xmlData)
        self.Latitude = xmlData.find('Latitude').text
        self.Longitude = xmlData.find('Longitude').text
        self.Precision = xmlData.find('Precision').text

class ReceiveCustomEventMsg(ReceiveEventMsg):
    pass