#给公众号创建菜单
import requests
import wechatBasic
from menu_data import menu_data
import json

def create_menu(access_token,json_menu):
    print(json_menu)
    json_menu = json.dumps(json_menu,ensure_ascii=False)
    create_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={0}'.format(access_token)
    response = requests.post(create_url,json_menu.encode('utf-8'))
    return json.loads(response.text)

def query_menu(access_token):
    query_url = 'https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s'% access_token
    response = requests.get(query_url)
    return json.loads(response.content)

def delete_menu(access_token):
    delete_url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s'% access_token
    response = requests.get(delete_url)
    return json.loads(response.text)


if __name__ == '__main__':
    access_token = wechatBasic.Basic().get_access_token()
    print(access_token)
    result = create_menu(access_token,menu_data)
   # result = query_menu(access_token)
  #  result = delete_menu(access_token)
    print(result)
