from django.test import TestCase
import xml.etree.ElementTree as ET
import requests
import json

appId = 'wx349372b8988f6776'  # 测试账号的appid 和 ssecret
appSecret = '842393f9522920ff375e3e50873c3c3c'
accesstoken_api = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.format(
    appId, appSecret
)
response = requests.get(accesstoken_api)
accessToken = json.loads(response.text, encoding='utf-8')
print(accessToken['access_token'])
print(accessToken['expires_in'])