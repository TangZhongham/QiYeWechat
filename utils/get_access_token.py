import requests


def get_access_token():
    """通过企业ID和应用Secret 获取 access_token"""

    ID = 'ww8059a2127f62bc2a'

    SECRET = 'm-ltxqrYwsJ2VXZ5ItM4jY8e2llCt7rkYWUn7-W1BOI'

    request_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(ID, SECRET)

    print(request_url)

    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) "\
                      "Chrome/71.0.3578.98 Safari/537.36",
    }

    a = requests.get(request_url, headers=headers)

    return_msg = a.json()
    print(return_msg['errcode'])

    if return_msg['errcode'] == 0:
        access_token = return_msg['access_token']
        print(access_token)
        return access_token
    else:
        pass


if __name__ == '__main__':
    get_access_token()