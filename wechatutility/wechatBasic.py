import requests
import time
import json
import wechat_Const

class Basic:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0

    def __real_get_accesstoken(self):
        appId =wechat_Const.appId
        appSecret = wechat_Const.appSecret
        #appId = 'wx4409cf14b491bef5'  # 我的appid 和 ssecret
      #  appSecret = '5d97ccc1119b3c4e50c8a3776d7a5ada'
        accesstoken_api = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.format(
            appId,appSecret
        )
        response = requests.get(accesstoken_api)
        accessToken = json.loads(response.text,encoding='utf-8')
        self.__accessToken = accessToken['access_token']
        self.__leftTime = accessToken['expires_in']

    def get_access_token(self):
        if self.__leftTime <10:
            self.__real_get_accesstoken()
        return self.__accessToken

    def run(self):
        while (True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()