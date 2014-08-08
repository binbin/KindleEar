#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, datetime
from bs4 import BeautifulSoup
from lib.urlopener import URLOpener
from base import BaseFeedBook
from lib.autodecoder import AutoDecoder

def getBook():
    return Studytimes

class Studytimes(BaseFeedBook):
    title                 = u'学习时报'
    description           = u'学习时报,每周一更新.'
    language              = 'zh-cn'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_studytimes.png"
    coverfile             = "cv_studytimes.png"
    network_timeout       = 150
    oldest_article        = 1
    deliver_days = ['Monday']
    force_ftitle          = True
    
    
    def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        link_search=re.compile(r"""gourl\((?:'|")(.+?)(?:'|")""").search
        urls = []
        url = r'http://www.studytimes.cn'
        def getPageContent(u_url):
            opener = URLOpener(self.host, timeout=self.timeout)
            result = opener.open(u_url)
            if result.status_code != 200 or not result.content:
                self.log.warn('fetch webpage failed(%d):%s.' % (result.status_code, u_url))
                return ''
                
            if self.feed_encoding:
                try:
                    content = result.content.decode(self.feed_encoding)
                except UnicodeDecodeError:
                    content = AutoDecoder(False).decode(result.content,opener.realurl,result.headers)
            else:
                content = AutoDecoder(False).decode(result.content,opener.realurl,result.headers)
            return content
        main_page = getPageContent(url)
        soup = BeautifulSoup(main_page, 'lxml')
        ul = soup.find('ul', attrs={'class':'list'})
        for a in ul.find_all('a'):
            t=a.string
            link = a['href']
            if 'http' not in link:
                link = 'http://www.studytimes.cn/%s'%link
            sub_page = getPageContent(link)
            s_soup = BeautifulSoup(sub_page, 'lxml')
            sub_ul = s_soup.find('ul', attrs={'class':'list'})
            for aa in sub_ul.find_all('a'):
                if 'javascript' in aa['href'] and aa['onclick']:
                   m = link_search(aa['onclick'])
                   if m:
                      l = m.group(1)
                      if 'http' not in l:
                         l = 'http://www.studytimes.cn%s'%l
                      urls.append(('%s%s'%(u'学习时报_',t),aa['title'].strip() or aa.string.strip(),l,None))
                else:
                    urls.append(('%s%s'%(u'学习时报_',t),aa['title'].strip() or aa.string.strip(),aa['href'],None))
        return urls

