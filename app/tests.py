from django.test import TestCase
import xml.etree.ElementTree as ET

teststr =b'''<xml>
<ToUserName><![CDATA[gh_ff0d9ce9cac3]]></ToUserName>\n
<FromUserName><![CDATA[ouRxO1KGnCdQ2ONHAwUwc98W_NMI]]></FromUserName>\n
<CreateTime>1576147191</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n
<Content><![CDATA[\xe6\x88\x91\xe4\xbb\xac]]></Content>\n<MsgId>22565001767429625</MsgId>\n</xml>'''

xmlData = ET.fromstring(teststr)
a = xmlData.find('MsgType').text
print(a)