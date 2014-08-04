#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, datetime
from bs4 import BeautifulSoup
from lib.urlopener import URLOpener
from base import BaseFeedBook
from lib.autodecoder import AutoDecoder
import re

def getBook():
    return Cctvnewoneplusone

class Cctvnewoneplusone(BaseFeedBook):
    title                 = u'新闻1+1'
    description           = u'央视新闻1+1'
    language              = 'zh-cn'
    # feed_encoding         = "utf-8"
    # page_encoding         = "utf-8"
    feed_encoding         = "gbk"
    page_encoding         = "gbk"
    mastheadfile          = "mh_news_cctv.jpg"
    coverfile             = "cv_news_cctv.jpg"
    network_timeout       = 60
    oldest_article        = 1

    def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        urls = []
        url = r'http://cctv.cntv.cn/lm/xinwenyijiayi/video/index.shtml'
        opener = URLOpener(self.host, timeout=self.timeout)
        result = opener.open(url)
        if result.status_code != 200 or not result.content:
            self.log.warn('fetch webpage failed(%d):%s.' % (result.status_code, url))
            return []
            
        if self.feed_encoding:
            try:
                content = result.content.decode(self.feed_encoding)
            except UnicodeDecodeError:
                content = AutoDecoder(False).decode(result.content,opener.realurl,result.headers)
        else:
            content = AutoDecoder(False).decode(result.content,opener.realurl,result.headers)
        
        list_pattern=re.compile(r'{\'title\':\'.*?\'<!--VIDEOSTR-->\'}', re.S)
        file_name_search=re.compile(r'\d{4}/\d{2}/\d{2}').search
        l=re.findall(list_pattern,content)
        tnow = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        for i in l[:5]:
            item=eval(i)
            try:
                pubdate = datetime.datetime.strptime(file_name_search(item["link_add"]).group(0), '%Y/%m/%d')
            except Exception as e:
                continue
            delta = tnow - pubdate
            if self.oldest_article > 0 and delta.days > self.oldest_article:
                  continue
            urls.append((u'新闻1+1',item['title'],item['link_add'],None))
        return urls
        