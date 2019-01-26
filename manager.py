from flask import Flask
from flask import request
from utils.get_access_token import get_access_token
import requests
import json
import sys
from configparser import ConfigParser


from .utils.WXBizMsgCrypt import WXBizMsgCrypt


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


@app.route('/auto-reply')
def auto_reply(msg):
    wxcpt = WXBizMsgCrypt(self.sToken, self.sEncodingAESKey, self.sCorpID)
    # 获取url验证时微信发送的相关参数
    sVerifyMsgSig = request.args.get('msg_signature')
    sVerifyTimeStamp = request.args.get('timestamp')
    sVerifyNonce = request.args.get('nonce')
    sVerifyEchoStr = request.args.get('echostr')

    # 验证url
    if request.method == 'GET':
        ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
        print
        type(ret)
        print
        type(sEchoStr)

        if (ret != 0):
            print
            "ERR: VerifyURL ret:" + str(ret)
            sys.exit(1)
        return sEchoStr

    # 接收客户端消息
    if request.method == 'POST':
        sReqMsgSig = sVerifyMsgSig
        sReqTimeStamp = sVerifyTimeStamp
        sReqNonce = sVerifyNonce
        sReqData = request.data
        print(sReqData)

        ret, sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        print
        ret, sMsg
        if (ret != 0):
            print
            "ERR: DecryptMsg ret: " + str(ret)
            sys.exit(1)
        # 解析发送的内容并打印

        xml_tree = ET.fromstring(sMsg)
        print('xml_tree is ', xml_tree)
    return "This is for auto-reply usage.\n {}".format(msg)


@app.route('/')
def auto():
    return "Hello world!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)