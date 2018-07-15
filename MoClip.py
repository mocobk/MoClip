# -*- coding:utf-8 -*-  
# __auth__ = mocobk
# email: mailmzb@qq.com
from os import path, mkdir
import threading
import keyboard
import time

from utils import Config
from utils.UpyunImg import UpImage
from utils.TencentOcr import AiPlat
from utils.Clipboard import *
from utils.notify import NotifyBubble

hostname = Config.UPYUN['hostname']
space = Config.UPYUN['space']
user = Config.UPYUN['user']
password = Config.UPYUN['password']
up_path = Config.UPYUN['up_path']
img_format = Config.UPYUN['img_format']
img_save_path = Config.UPYUN['img_save_path']

app_key = Config.TENCENT_OCR['app_key']
app_id = Config.TENCENT_OCR['app_id']

image_format = Config.IMAGE_FORMAT

if not path.exists(img_save_path):
    mkdir(img_save_path)


def img2markdown():
    markdown_url = '![image]({})'
    image_path_list = _get_img_local_path()
    markdown_url_list = []
    for item in image_path_list:
        markdown_url_list.append(markdown_url.format(_up_img(item)))
    return '\n'.join(markdown_url_list)


def img2text():
    image_path_list = _get_img_local_path()
    ai_plat = AiPlat(app_id, app_key)
    text_list = []
    for item in image_path_list:
        with open(item, 'rb') as bin_data:
            image_data = bin_data.read()
            text = ai_plat.getOcrText(image_data)
            text_list.append(text)
    return ''.join(text_list)


def _get_img_local_path():
    image_path_list = []
    image_obj = get_clipboard_image()
    if image_obj:
        # timestamp = time.strftime('%Y%m%d%H%M%S')
        # save_path = img_save_path + '/img' + timestamp + '.jpg'
        save_path = img_save_path + '/temp_img.jpg'
        image_obj.save(save_path)
        image_path_list.append(save_path)
    else:
        img_list = get_clipboard_files()
        for each in img_list:
            if path.splitext(each)[1] in image_format:
                image_path_list.append(each)
    return image_path_list


def _up_img(img_path):
    up = UpImage(space, user, password)
    response = up.upimage(img_path, up_path, img_format=img_format)
    return hostname + response['url']


def _set_clipboard(func):
    _notify('MoClip', '图片正在上传...')
    text = func()
    set_clipboard_text(text)
    log = 'info [{0}] {1}'
    print(log.format(time.strftime('%H:%M:%S'), text))
    _notify('复制至剪贴板', 'Sucess!')


def _notify(title, msg):
    notify = NotifyBubble()
    notify.showMsg(title, msg, show_time=2)


def key_listener():
    keyboard.add_hotkey('alt+f1', _set_clipboard, args=(img2markdown,))
    keyboard.add_hotkey('alt+f2', _set_clipboard, args=(img2text,))
    keyboard.wait()


def main():
    print('MoClip starting...')
    print('Press Alt + F1 generate markdown text')
    print('Press Alt + F2 generate ocr text')
    print('Then, you can press Ctrol + V  to paste it any where\n')
    hot_key_thread = threading.Thread(target=key_listener)
    hot_key_thread.setDaemon(True)
    hot_key_thread.start()
    hot_key_thread.join()


if __name__ == '__main__':
    # print(img2markdown())
    # print(img2text())
    main()
