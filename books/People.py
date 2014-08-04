#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, datetime
from bs4 import BeautifulSoup
from lib.urlopener import URLOpener
from base import BaseFeedBook
from lib.autodecoder import AutoDecoder

def getBook():
    return People

class People(BaseFeedBook):
    title                 = u'人民网要闻要论'
    description           = u'人民网要闻要论(含人民日报)'
    language              = 'zh-cn'
    # feed_encoding         = "utf-8"
    # page_encoding         = "utf-8"
    feed_encoding         = "gbk"
    page_encoding         = "gbk"
    mastheadfile          = "mh_people.gif"
    coverfile             = "cv_people.jpg"
    network_timeout       = 60
    oldest_article        = 1

    def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        urls = []
        url = r'http://opinion.people.com.cn/GB/40604/index.html'
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

        box=soup.find('div', attrs={'class':'p2j_list'})
        for li in box.find_all('li'):
            a=li.find('a')
            # print a['href'],a.string
            title = a.string
            if u'人民日报' in title:
                urls.append((u'人民日报',a.string,r'%s%s'%(r'http://opinion.people.com.cn',a['href']),None))
            else:
                urls.append((u'人民网',a.string,r'%s%s'%(r'http://opinion.people.com.cn',a['href']),None))
        return urls

