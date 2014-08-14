#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, datetime
from bs4 import BeautifulSoup
from lib.urlopener import URLOpener
from base import BaseFeedBook
from lib.autodecoder import AutoDecoder
import datetime


def getBook():
    return Banyuetan

class Banyuetan(BaseFeedBook):
    title                 = u'半月谈'
    description           = u'半月谈_中共中央宣传部委托新华通讯社主办'
    language              = 'zh-cn'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "cv_banyuetan.gif"
    coverfile             = "cv_banyuetan.gif"
    network_timeout       = 60
    oldest_article        = 1
    
    feeds = [ (u'半月谈_时政_为政者说_访谈','http://www.banyuetan.org/chcontent/sz/wzzs/szft/index.html'),
              (u'半月谈_时政_为政者说_笔谈','http://www.banyuetan.org/chcontent/sz/wzzs/szbt/index.html'),
              (u'半月谈_时政_为政者说_诤言','http://www.banyuetan.org/chcontent/sz/wzzs/szgd/index.html'),
              (u'半月谈_时政_时政聚焦','http://www.banyuetan.org/chcontent/sz/szgc/index.html'),
              (u'半月谈_时政_环球看点','http://www.banyuetan.org/chcontent/sz/hqkd/index.html'),
              (u'半月谈_时政_经济观察','http://www.banyuetan.org/chcontent/sz/jjzs/index.html'),
              (u'半月谈_资讯_要闻300秒','http://www.banyuetan.org/chcontent/zx/yw/index.html'),
              (u'半月谈_资讯_媒体集萃','http://www.banyuetan.org/chcontent/zx/mtzd/index.html'),
              (u'半月谈_资讯_民生话题','http://www.banyuetan.org/chcontent/zx/shxw/index.html'),
              (u'半月谈_政策_最新政策','http://www.banyuetan.org/chcontent/zc/zxzc/index.html'),
              (u'半月谈_政策_政策解读','http://www.banyuetan.org/chcontent/zc/zcjd/index.html'),
              (u'半月谈_政策_政策咨询','http://www.banyuetan.org/chcontent/zc/zczx/index.html'),
              (u'半月谈_政策_曝光台','http://www.banyuetan.org/chcontent/zc/bgt/index.html'),
              (u'半月谈_政策_民声','http://www.banyuetan.org/chcontent/zc/ms/index.html'),
              (u'半月谈_观点_评论','http://www.banyuetan.org/chcontent/gd/pl/index.html'),
              (u'半月谈_观点_专栏作家','http://www.banyuetan.org/chcontent/gd/zlzj/index.html'),
              (u'半月谈_观点_人物','http://www.banyuetan.org/chcontent/gd/sdrw/index.html')
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
            box=soup.find('div', attrs={'class':'list_cont_li'})
            for li in box.find_all('li'):
                a=li.find('a')
                if not a:
                  continue
                pubdate = li.find('span')
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
                    urls.append((feed[0],a.string,r'%s%s'%(r'http://www.banyuetan.org',a['href']),None))
        return urls

