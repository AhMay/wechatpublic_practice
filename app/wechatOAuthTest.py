from wechatutility.wechat_OauthProcess import *

class wechatOAuthTest(object):
    def getUserInfo(self, code):
        token_info = exchange_access_token(code)
        userinfo = query_userinfo(token_info['access_token'],token_info['openid'])
        return userinfo