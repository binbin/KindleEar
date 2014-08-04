#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, datetime
from bs4 import BeautifulSoup
from lib.urlopener import URLOpener
from base import BaseFeedBook
from lib.autodecoder import AutoDecoder
import datetime


def getBook():
    return Cnrnews

class Cnrnews(BaseFeedBook):
    title                 = u'央广网新闻及评论'
    description           = u'央广网新闻及评论'
    language              = 'zh-cn'
    feed_encoding         = "gbk"
    page_encoding         = "gbk"
    mastheadfile          = "mh_cnrnews.jpg"
    coverfile             = "cv_cnrnews.jpg"
    network_timeout       = 60
    oldest_article        = 1
    
    feeds = [ (u'央广网评论_央广观察','http://news.cnr.cn/comment/latest/'),
              (u'央广网评论_相对论','http://news.cnr.cn/comment/view/'),
              (u'中国之声_新闻纵横','http://china.cnr.cn/yaowen/')
            ]
    def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        urls = []
        tnow = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        for feed in self.feeds:
            url = feed[1]
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
            box=soup.find('div', attrs={'class':'sanji_left'})
            for li in box.find_all('li'):
                a=li.find('a')
                if not a:
                  continue
                pubdate = li.contents[1]
                if not pubdate:
                    continue 
                try:
                    pubdate = datetime.datetime.strptime(pubdate.string, '%Y-%m-%d %H:%M')
                except Exception as e:
                    # self.log.warn('parse pubdate failed for [%s] : %s'%(url,str(e)))
                    continue
                delta = tnow - pubdate
                if self.oldest_article > 0 and delta.days > self.oldest_article:
                  continue
                # print a['href'],a.string.replace('<b>','').replace('</b>','')
                if r'http://' in a['href']:
                    urls.append((feed[0],a.string,a['href'],None))
                else:
                    urls.append((feed[0],a.string,r'%s%s'%(r'http://news.cnr.cn',a['href']),None))
        return urls

