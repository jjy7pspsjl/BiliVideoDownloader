# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/12/12 13:00
# software : PyCharm

import os

from config import UrlConfig, PathConfig


class CreateFolder(object):
    """Create a folder, if it does not exist."""
    for key in UrlConfig.RANKING_DICT:
        if not os.path.exists(f'{PathConfig.FILE_PATH}\\{UrlConfig.RANKING_DICT[key]}'):
            os.mkdir(f'{PathConfig.FILE_PATH}\\{UrlConfig.RANKING_DICT[key]}')
