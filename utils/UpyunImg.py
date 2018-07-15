# -*- coding:utf-8 -*-  
# __auth__ = mocobk
# email: mailmzb@qq.com
import time
import upyun
from os import path


class UpImage:
    def __init__(self, space, user, password):
        # 创建实例，api文档http://docs.upyun.com/api/sdk/#python-sdk
        self.up = upyun.UpYun(space, user, password)
        # up.mkdir('/image')  # 创建目录
        # up.delete('/up/temp/')  # 删除目录
        # 将图片转未webp格式，减少体积，但保存后需要浏览器打开，更多功能见api

    def upimage(self, img_path, upload_path, img_format='webp'):
        headers = {'x-gmkerl-thumb': '/format/%s' % img_format}
        if path.exists(img_path):
            with open(img_path, 'rb') as fp:
                timestamp = time.strftime('%Y%m%d%H%M%S')
                up_path = upload_path + '/img' + timestamp + '.' + img_format
                response = self.up.put(up_path, fp, headers=headers)
                response['url'] = up_path
                return response
        else:
            return 'File not exists!', img_path


if __name__ == '__main__':
    space, user, password = 'xxx', 'xxx', 'xxx'
    up = UpImage(space, user, password)
    r = up.upimage('shouxie.jpg', '/image', img_format='jpg')
    print(r)
