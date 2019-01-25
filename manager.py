from flask import Flask
from utils.get_access_token import get_access_token
import requests
import json


app = Flask(__name__)


@app.route('/<msg_text>')
def index(msg_text):
    ac_token = get_access_token()
    if ac_token:
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + ac_token
        msg = {
            "touser": "@all",
            "toparty": "",
            "totag": "",
            "msgtype": "text",
            "agentid": 1000002,
            "text": {
                "content": msg_text
            },
            "safe": 0,
        }
        msg_send = requests.post(url, data=json.dumps(msg))
        a = msg_send.text
        print(a)
        if a:
            return "<h1> success </h1>\n%s" % a


if __name__ == '__main__':
    app.run(debug=True)