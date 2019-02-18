from flask import request, abort, Blueprint, url_for, redirect

from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from wechatpy.enterprise import parse_message, create_reply


TOKEN = 'lw2blf8'
EncodingAESKey = '6ObhL0l5EmsGUYDaeJgKyxqAH7ixraGEJFmO9FJieWP'
APPID = '1000002'
CorpId = 'ww8059a2127f62bc2a'


receive_msg = Blueprint('receive_msg', __name__)


@receive_msg.route('/receive', methods=['GET', 'POST'])
def receive_msg():
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
            print('Success')
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
