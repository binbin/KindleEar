#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, datetime
from bs4 import BeautifulSoup
from lib.urlopener import URLOpener
from base import BaseFeedBook
from lib.autodecoder import AutoDecoder
import datetime


def getBook():
    return QstheorySubject

class QstheorySubject(BaseFeedBook):
    title                 = u'求是理论网_专题'
    description           = u'求是理论网_专题'
    language              = 'zh-cn'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_qstheory_subject.jpg"
    coverfile             = "cv_qstheory_subject.jpg"
    network_timeout       = 60
    oldest_article        = 1

    feeds = [ (u'求是_热点聚焦','http://www.qstheory.cn/was5/web/search?channelid=288671&prepage=10&searchword=extend5%3D%27%251184339%25%27&list=1184339'),
              (u'求是_求是导读','http://www.qstheory.cn/was5/web/search?channelid=288671&searchword=extend5%3D%27%251184341%25%27&prepage=10&list=1184341'),
              (u'求是_热点话题','http://www.qstheory.cn/was5/web/search?channelid=288671&prepage=10&searchword=extend5%3D%27%251184553%25%27&list=1184553'),
              (u'求是_热点导读','http://www.qstheory.cn/was5/web/search?channelid=268219&prepage=30&searchword=extend5%3D%27%251181640%25%27&list=1181640'),
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

            file_name_search=re.compile(r'\d{4}-\d{2}/\d{2}').search
            tnow = datetime.datetime.utcnow()+datetime.timedelta(hours=8)

            list_article = soup.find_all('h3')
            if not list_article:
                list_article = soup.find_all('h2')

            for h3 in list_article:
                a=h3.find('a')
                if not a:
                  continue
                href = a['href']
                try:
                    m=file_name_search(href)
                    if m:
                        pubdate = datetime.datetime.strptime(m.group(0), '%Y-%m/%d')
                    else:
                        continue
                except Exception as e:
                    self.log.warn('parse pubdate failed for [%s] : %s'%(url,str(e)))
                    continue
                delta = tnow - pubdate
                if self.oldest_article > 0 and delta.days > self.oldest_article:
                  continue

                if r'http://' in a['href']:
                    urls.append((feed[0],a.string,a['href'],None))
                else:
                    urls.append((feed[0],a.string,r'%s%s'%(r'http://www.qstheory.cn',a['href']),None))
        return urls

    def fetcharticle(self, url, opener, decoder):
        """ 有分页，在此函数内下载全部分页，合并成一个单独的HTML返回。"""
        result = opener.open("http://www.instapaper.com/m?u=%s"%self.url_unescape(url))
        status_code, content = result.status_code, result.content
        if status_code != 200 or not content:
            self.log.warn('fetch article failed(%d):%s.' % (status_code,url))
            return None
        
        if self.page_encoding:
            try:
                firstpart = content.decode(self.page_encoding)
            except UnicodeDecodeError:
                firstpart = decoder.decode(content,opener.realurl,result.headers)
        else:
            firstpart = decoder.decode(content,opener.realurl,result.headers)
        
        article_urls = []
        soup = BeautifulSoup(firstpart, "lxml")

        def clear_pager(s):
            temp_listpage = s.find('center')
            if temp_listpage:
                temp_divs = listpage.find_all('div')
                if temp_divs and len(temp_divs) == 2:
                    temp_listpage.decompose()

        article = soup.find('div', attrs={'id':'story'})#.find_all('div')[0]
        if not article:
            return None
        listpage = soup.find('center')    
        if listpage: 
            divs = listpage.find_all('div')
            if divs and len(divs) == 2:#有分页
                links = divs[0].find_all('a')
                for parturl in links[:-1]:
                    article_urls.append(parturl['href'])
                    # self.log.warn('page url %s'%parturl['href'])
            # return ''.join(map(lambda x:self.fetch("http://www.instapaper.com/m?u=%s"%self.url_unescape(x), opener, decoder) or '',article_urls))
            # return ''.join(map(lambda x:self.fetch(x, opener, decoder) or '',article_urls))
                pages_contents=map(lambda x:self.fetch("http://www.instapaper.com/m?u=%s"%self.url_unescape(x), opener, decoder) or '',article_urls)
                for page in pages_contents:
                    temp_soup = BeautifulSoup(page, "lxml")
                    clear_pager(temp_soup)
                    story = temp_soup.find('div', attrs={'id':'story'})
                    if story:
                        # article1=story.find_all('div')[0]
                        # article1.insert_after(article)
                        # story.insert_after(article)
                        article.append(story.find_all('div')[0])
                    else:
                        self.log.warn('get page content error %s'%"http://www.instapaper.com/m?u=%s"%self.url_unescape(url))
        clear_pager(soup)
        return unicode(soup)

'''
    def fetcharticle(self, url, opener, decoder):
        """ 有分页，在此函数内下载全部分页，合并成一个单独的HTML返回。"""
        result = opener.open(url)
        status_code, content = result.status_code, result.content
        if status_code != 200 or not content:
            self.log.warn('fetch article failed(%d):%s.' % (status_code,url))
            return None
        
        #内嵌函数，用于处理分页信息
        def not_is_thispage(tag):
            return not tag.has_attr('class')
        
        if self.page_encoding:
            try:
                firstpart = content.decode(self.page_encoding)
            except UnicodeDecodeError:
                firstpart = decoder.decode(content,opener.realurl,result.headers)
        else:
            firstpart = decoder.decode(content,opener.realurl,result.headers)
        
        otherparts = []
        soup = BeautifulSoup(firstpart, "lxml")
        listpage = soup.find('div', attrs={'class':'div_currpage'})
        if listpage: #有分页
            for parturl in listpage.find_all('a')[:-1]:
                parturl = self.urljoin(url, parturl['href'])
                result = opener.open(parturl)
                status_code, content = result.status_code, result.content
                if status_code != 200 or not content:
                    self.log.warn('fetch article failed(%d):%s.' % (status_code,url))
                else:
                    if self.page_encoding:
                        try:
                            thispart = content.decode(self.page_encoding)
                        except UnicodeDecodeError:
                            thispart = decoder.decode(content,parturl,result.headers)
                    else:
                        thispart = decoder.decode(content,parturl,result.headers)
                    otherparts.append(thispart)
                        
            #合并文件后不再需要分页标志
            listpage.parent.parent.decompose()
            
        #逐个处理各分页，合成一个单独文件
        article1 = soup.find('div', attrs={'id':'content'})
        if not article1:
            return None
        
        
        #将其他页的文章内容附加到第一页的文章内容后面
        for page in otherparts[::-1]:
            souppage = BeautifulSoup(page, "lxml")
            article = souppage.find('div', attrs={'id':'content'})
            if not article:
                continue
                            
            article1.insert_after(article)
        
        for div in soup.find_all('div',attrs={'class':'backtop'}):
            div.decompose()
        
        return unicode(soup)

'''