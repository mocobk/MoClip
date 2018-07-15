# -*- coding: UTF-8 -*-
import base64
import hashlib
import time
import urllib

import requests


class AiPlat(object):
    url_preffix = 'https://api.ai.qq.com/fcgi-bin/'

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.data = {}
        self.url_data = ''
        self.url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr'

    def invoke(self, params):
        try:
            rsp = requests.post(self.url, data=params)
            dict_rsp = rsp.json()
            return dict_rsp
        except Exception as e:
            dict_error = {'ret': -1, 'httpcode': -1, 'msg': e}
            return dict_error

    def getOcrGeneralocr(self, image):
        """ocr识别"""
        image_data = base64.b64encode(image)
        self.data = {
            'app_id': self.app_id,
            'app_key': self.app_key,
            'time_stamp': int(time.time()),
            'nonce_str': int(time.time()),
            'image': image_data.decode('utf-8'),
        }
        sign_str = self.genSignString(self.data)
        self.data['sign'] = sign_str
        return self.invoke(self.data)

    def getOcrText(self, image):
        response = self.getOcrGeneralocr(image)
        string_list = [item['itemstring'] for item in response['data']['item_list']]
        if response['ret'] == 0:
            text = '\n'.join(string_list)
            return text
        else:
            return 'Error', response

    @staticmethod
    def genSignString(parser):
        uri_str = ''
        for key in sorted(parser.keys()):
            if key == 'app_key':
                continue
            uri_str += "%s=%s&" % (key, urllib.parse.quote(str(parser[key]), safe=''))
        sign_str = uri_str + 'app_key=' + parser['app_key']
        hash_md5 = hashlib.md5(sign_str.encode("utf8"))
        return hash_md5.hexdigest().upper()


if __name__ == '__main__':
    app_key = 'xxx'
    app_id = 'xxxx'
    with open('generalocr.jpg', 'rb') as bin_data:
        image_data = bin_data.read()
    ai_plat = AiPlat(app_id, app_key)
    rsp = ai_plat.getOcrText(image_data)
    print(rsp)
