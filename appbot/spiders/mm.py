﻿# -*- coding: utf-8 -*-
import scrapy
import re
import urllib
import codecs

def clean_sub(symbol, app_name):
    str = symbol.decode('utf-8')
    str_index = app_name.find(str)
    if str_index > 0:
        app_name = app_name[0:str_index]
    return app_name


def clean_app_name(app_name):
    space = u'\u00a0'
    app_name = app_name.replace(space, '')

    app_name = clean_sub('-', app_name)
    app_name = clean_sub('（', app_name)
    app_name = clean_sub('：', app_name)

    brackets = r'\(.*\)|\[.*\]|【.*】|（.*）'
    return re.sub(brackets, '', app_name).replace('\r\n', '')

def get_kw_url(kw):
    base_url = u'http://mm.10086.cn/searchapp?q=%s'
    kw = clean_app_name(kw)
    return base_url % (urllib.quote(kw.encode("utf8")))

class AppbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    key_word = scrapy.Field()
    search_word = scrapy.Field()
    first_search_result = scrapy.Field()
    version = scrapy.Field()
    pass


class MM(scrapy.Spider):
    name = "mm"
    allowed_damains = ['http://mm.10086.cn/']


    def start_requests(self):
        with codecs.open('./input/appName.txt', 'r', 'utf-8') as f:
            for app_name in f:
                self.log(get_kw_url(app_name))
                yield scrapy.Request(url=get_kw_url(app_name),
                    callback = self.parse_search_result,
                    meta = {'kw' : app_name.strip(),
                    'search_word' : clean_app_name(app_name)})

        pass

    def parse_search_result(self, response):

        next_page_url = response.css('body>div.search_content>div.content>div>div.content_list_cont>div:nth-child(1)>div>a::attr(href)').extract_first() 



        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url),
                callback = self.parse,
                meta = response.meta)
            pass
        else:
            yield {
                'key_word' : response.meta['kw'],
                'search_word' : response.meta['search_word'],
                'first_search_result' : '找不到', 
                'version' : '找不到'
            }

    def parse(self, response):

        # debug error : 'NoneType' object has no attribute 'strip' 
        first_search_result_css = response.css('body>div.mj_cont>div.mj_cont_right.mj_shadow>div.mj_cont_right_top>div.mj_cont_right_top_l>div.mj_big_title.font-f-yh>span::text').extract_first()
        version_css = response.css('body > div.mj_cont > div.mj_cont_left.mj_shadow > div.mj_info.font-f-yh > ul > li:nth-child(3)::text').extract_first()
        if first_search_result_css is not None:
            first_search_result = first_search_result_css.strip()
            pass
        else:
            first_search_result = '需重新抓取'
            pass

        if version_css is not None:
            version = re.sub(r'[^0-9.]', '', version_css.strip())
            pass
        else:
            version = '需重新抓取'
            pass

        yield {
            'key_word' : response.meta['kw'],
            'search_word' : response.meta['search_word'],
            'first_search_result' :  first_search_result,
            'version' : version
            }