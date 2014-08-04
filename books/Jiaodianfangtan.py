#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, datetime
from bs4 import BeautifulSoup
from lib.urlopener import URLOpener
from base import BaseFeedBook
from lib.autodecoder import AutoDecoder
import re

def getBook():
    return Jiaodianfangtan

class Jiaodianfangtan(BaseFeedBook):
    title                 = u'焦点访谈'
    description           = u'央视焦点访谈'
    language              = 'zh-cn'
    # feed_encoding         = "utf-8"
    # page_encoding         = "utf-8"
    feed_encoding         = "gbk"
    page_encoding         = "gbk"
    mastheadfile          = "mh_jiaodianfangtan.jpg"
    coverfile             = "cv_jiaodianfangtan.jpg"
    network_timeout       = 60
    oldest_article        = 1

    def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        urls = []
        url = r'http://cctv.cntv.cn/lm/jiaodianfangtan/index.shtml'
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

        soup = BeautifulSoup(content, 'lxml')
        file_name_search=re.compile(r'\d{4}/\d{2}/\d{2}').search
        tnow = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        for li in soup.find_all('div', attrs={'class':'text'}):
            a=li.find('a')
            href = a['href']
            try:
                pubdate = datetime.datetime.strptime(file_name_search(href).group(0), '%Y/%m/%d')
            except Exception as e:
                continue
            delta = tnow - pubdate
            if self.oldest_article > 0 and delta.days > self.oldest_article:
                  continue
            urls.append((u'焦点访谈',a.string,href,None))
        return urls
        