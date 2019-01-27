from flask import Flask
from flask import request, abort
from utils.get_access_token import get_access_token
import requests
import json
import sys
from configparser import ConfigParser

from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from wechatpy.enterprise import parse_message, create_reply


TOKEN = 'lw2blf8'
EncodingAESKey = '6ObhL0l5EmsGUYDaeJgKyxqAH7ixraGEJFmO9FJieWP'
APPID = '1000002'
CorpId = 'ww8059a2127f62bc2a'


app = Flask(__name__)


@app.route('/msg/<msg_text>')
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
        else:
            return "failed"


@app.route('/auto', methods=['GET', 'POST'])
def auto_reply():
    signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')

    crypto = WeChatCrypto(TOKEN, EncodingAESKey, CorpId)
    if request.method == 'GET':
        echo_str = request.args.get('echostr', '')
        try:
            echo_str = crypto.check_signature(
                signature,
                timestamp,
                nonce,
                echo_str
            )
            print(echo_str)
        except InvalidSignatureException:
            abort(403)
        return echo_str
    else:
        try:
            msg = crypto.decrypt_message(
                request.data,
                signature,
                timestamp,
                nonce
            )
            msg = parse_message(msg)
            if msg.type == 'text':
                reply = create_reply(msg.content, msg).render()
            else:
                reply = create_reply('Can not handle this for now', msg).render()
            res = crypto.encrypt_message(reply, nonce, timestamp)
            return res
        except (InvalidSignatureException, InvalidCorpIdException):
            abort(403)


@app.route('/')
def auto():
    return "Hello world!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)