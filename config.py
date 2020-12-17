# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/12/12 13:43
# software : PyCharm

"""全局变量存放于此"""

import os


class UrlConfig(object):
    """Url"""
    URL_HEAD = 'https://www.bilibili.com/video/'

    # 分支动态URL
    DYNAMIC_URL = 'https://api.bilibili.com/x/web-interface/dynamic/region?ps=15&rid={}'
    # 排行 URL day 对应是近几天的内容，可选(3 和 7),original 对应的是 全部(0) 或 原创(1)
    RANKING_URL = 'https://api.bilibili.com/x/web-interface/ranking/region?day=3&original=0&rid={}'

    ITEMS_URLS = {
        '201': [DYNAMIC_URL.format(201), RANKING_URL.format(201)],
        '124': [DYNAMIC_URL.format(124), RANKING_URL.format(124)],
        '207': [DYNAMIC_URL.format(207), RANKING_URL.format(207)],
        '208': [DYNAMIC_URL.format(208), RANKING_URL.format(208)],
        '209': [DYNAMIC_URL.format(209), RANKING_URL.format(209)],
        '122': [DYNAMIC_URL.format(122), RANKING_URL.format(122)],
        '100': ['https://www.bilibili.com/v/technology'],
    }
    # rid 对应的 板块，创建文件夹用
    RANKING_DICT = {
        '122': '野生技术协会',
        '124': '社科人文',
        '201': '科学科普',
        '207': '财经',
        '208': '校园学习',
        '209': '职业职场',
        '100': '首页'
    }


class HeadersConfig(object):
    """Headers."""
    HEADERS = {
        'Referer': 'https://www.bilibili.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    VIDEO_HEADERS = {
        'accept': '*/*',
        'accept-encoding': 'identity',
        'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
        'origin': 'https://www.bilibili.com',
        # 'range': 'bytes=0-524288000',  # Max 500MB
        'range': 'bytes=0-10',  # Max 500MB
        'referer': 'https://www.bilibili.com/video/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }


class PathConfig(object):
    """Path."""
    # 建立项目根目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 建立视频默认存储路径
    FILE_PATH = os.path.join(BASE_DIR, r'spiderFrame\Download')
    FFMPEG_PATH = os.path.join(BASE_DIR, r'spiderFrame\ffmpeg\ffmpeg.exe')
