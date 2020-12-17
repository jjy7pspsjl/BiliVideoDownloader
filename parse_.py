# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/12/12 15:40
# software : PyCharm

"""Parse html or json program."""

import re
import json

from parsel import Selector


class ParseUrl:
    """Parse Bili url."""

    async def parse_str(self, html: str):
        sel = Selector(html)
        _xpath = r"//div[@class='groom-module']"
        urls = [url.split('/')[-1] for url in sel.xpath(f"{_xpath}/a/@href").getall()]
        return urls

    async def parse_json(self, html: dict):
        if isinstance(html['data'], list):
            result = [_data['bvid'] for _data in html['data']]
            return result
        if isinstance(html['data'], dict):
            result = [_data['bvid'] for _data in html['data']['archives']]
            return result

    async def main(self, html):
        if isinstance(html, str):
            result = await self.parse_str(html)
            return result
        if isinstance(html, dict):
            result = await self.parse_json(html)
            return result


class ParseHtml:
    """Parse Bili html"""
    async def parse(self, html):
        urlData = json.loads(re.findall('<script>window.__playinfo__=(.*?)</script>', html, re.M)[0])
        videoUrl = urlData['data']['dash']['video'][0]['baseUrl']
        audioUrl = urlData['data']['dash']['audio'][0]['baseUrl']
        fileName = re.findall('<h1 title="(.*?)" class="video-title">', html, re.M)[0]
        return fileName, videoUrl, audioUrl

    async def main(self, html):
        result = await self.parse(html)
        return result


async def parseUrl(html):
    parse = ParseUrl()
    result = await parse.main(html)
    return result


async def parseHtml(html):
    parse = ParseHtml()
    result = await parse.main(html)
    return result
