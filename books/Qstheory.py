#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re, datetime
from bs4 import BeautifulSoup
from lib.urlopener import URLOpener
from base import BaseFeedBook
from lib.autodecoder import AutoDecoder
import datetime


def getBook():
    return Qstheory

class Qstheory(BaseFeedBook):
    title                 = u'求是理论网_日常更新'
    description           = u'求是理论网_日常更新'
    language              = 'zh-cn'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_qstheory.gif"
    coverfile             = "cv_qstheory.png"
    network_timeout       = 60
    oldest_article        = 1
    force_ftitle          = True
    
    feeds = [   (u'求是理论网',u'头条推荐','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251184411%25%27&list=1184411'),
                (u'求是理论网',u'要闻','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181546%25%27&list=1181546'),
                (u'求是理论网',u'重要文章','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251184334%25%27&list=1184334'),
                (u'求是理论网',u'《求是》重点文章','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181551%25%27&list=1181551'),
                (u'求是理论网',u'《红旗文稿》推荐','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181552%25%27&list=1181552'),
                (u'求是理论网',u'原创精选','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251184643%25%27&list=1184643'),
                (u'求是理论网_经济',u'改革发展','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181614%25%27&list=1181614'),
                (u'求是理论网_经济',u'经济观察','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181615%25%27&list=1181615'),
                (u'求是理论网_经济',u'三农在线','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181616%25%27&list=1181616'),
                (u'求是理论网_经济',u'产业纵横','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181617%25%27&list=1181617'),
                (u'求是理论网_经济',u'热点解读','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181618%25%27&list=1181618'),
                (u'求是理论网_经济',u'新锐视点','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181619%25%27&list=1181619'),
                (u'求是理论网_经济',u'区域经济','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181620%25%27&list=1181620'),
                (u'求是理论网_经济',u'环球视野','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181621%25%27&list=1181621'),
                (u'求是理论网_经济',u'企业参考','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181622%25%27&list=1181622'),
                (u'求是理论网_经济',u'学术动态','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181623%25%27&list=1181623'),
                (u'求是理论网_政治',u'理论阵地','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181632%25%27&list=1181632'),
                (u'求是理论网_政治',u'改革探索','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181633%25%27&list=1181633'),
                (u'求是理论网_政治',u'观察思考','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181634%25%27&list=1181634'),
                (u'求是理论网_政治',u'民主政治','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181635%25%27&list=1181635'),
                (u'求是理论网_政治',u'依法治国','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181636%25%27&list=1181636'),
                (u'求是理论网_政治',u'行政管理','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181637%25%27&list=1181637'),
                (u'求是理论网_政治',u'学术研究','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181638%25%27&list=1181638'),
                (u'求是理论网_政治',u'史海钩沉','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181639%25%27&list=1181639'),
                (u'求是理论网_政治',u'网文推荐','http://www.qstheory.cn/was5/web/search?channelid=268219&prepage=30&searchword=extend5%3D%27%251181640%25%27&list=1181640'),
                (u'求是理论网_文化',u'文化强国','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181648%25%27&list=1181648'),
                (u'求是理论网_文化',u'核心价值','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181649%25%27&list=1181649'),
                (u'求是理论网_文化',u'体制改革','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181650%25%27&list=1181650'),
                (u'求是理论网_文化',u'文化产业','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181652%25%27&list=1181652'),
                (u'求是理论网_文化',u'文化事业','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181653%25%27&list=1181653'),
                (u'求是理论网_文化',u'文化视窗','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181656%25%27&list=1181656'),
                (u'求是理论网_文化',u'文化观察','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181655%25%27&list=1181655'),
                (u'求是理论网_文化',u'文艺评论','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181657%25%27&list=1181657'),
                (u'求是理论网_文化',u'金沙滩','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181651%25%27&list=1181651'),
                (u'求是理论网_文化',u'学术纵横','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181658%25%27&list=1181658'),
                (u'求是理论网_社会',u'资讯','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181664%25%27&list=1181664'),
                (u'求是理论网_社会',u'社会管理','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181665%25%27&list=1181665'),
                (u'求是理论网_社会',u'社会研究','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181666%25%27&list=1181666'),
                (u'求是理论网_社会',u'社会保障','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181667%25%27&list=1181667'),
                (u'求是理论网_社会',u'民生建设','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181668%25%27&list=1181668'),
                (u'求是理论网_社会',u'城乡发展','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181669%25%27&list=1181669'),
                (u'求是理论网_社会',u'人口工作','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181670%25%27&list=1181670'),
                (u'求是理论网_社会',u'学术前沿','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181671%25%27&list=1181671'),
                (u'求是理论网_社会',u'实践探索','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181672%25%27&list=1181672'),
                (u'求是理论网_社会',u'评论','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181673%25%27&list=1181673'),
                (u'求是理论网_社会',u'视野','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181674%25%27&list=1181674'),
                (u'求是理论网_党建',u'党建研究','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181686%25%27&list=1181686'),
                (u'求是理论网_党建',u'基层党建','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181687%25%27&list=1181687'),
                (u'求是理论网_党建',u'反腐倡廉','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181688%25%27&list=1181688'),
                (u'求是理论网_党建',u'执政能力','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181689%25%27&list=1181689'),
                (u'求是理论网_党建',u'群众工作','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181690%25%27&list=1181690'),
                (u'求是理论网_党建',u'观察思考','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181691%25%27&list=1181691'),
                (u'求是理论网_党建',u'实践探索','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181692%25%27&list=1181692'),
                (u'求是理论网_党建',u'党刊文萃','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181693%25%27&list=1181693'),
                (u'求是理论网_党建',u'党报视点','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181694%25%27&list=1181694'),
                (u'求是理论网_党建',u'党史博览','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181695%25%27&list=1181695'),
                (u'求是理论网_科教',u'科技观察','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181722%25%27&list=1181722'),
                (u'求是理论网_科教',u'科学普及','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181723%25%27&list=1181723'),
                (u'求是理论网_科教',u'创新前沿','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181724%25%27&list=1181724'),
                (u'求是理论网_科教',u'教育视点','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181725%25%27&list=1181725'),
                (u'求是理论网_科教',u'教育实践','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181726%25%27&list=1181726'),
                (u'求是理论网_科教',u'人才强国','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181727%25%27&list=1181727'),
                (u'求是理论网_科教',u'科教人物','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181728%25%27&list=1181728'),
                (u'求是理论网_科教',u'科教评论','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181729%25%27&list=1181729'),
                (u'求是理论网_科教',u'科教博文','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181730%25%27&list=1181730'),
                (u'求是理论网_科教',u'域外传真','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181731%25%27&list=1181731'),
                (u'求是理论网_生态',u'资讯','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181706%25%27&list=1181706'),
                (u'求是理论网_生态',u'时评','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181707%25%27&list=1181707'),
                (u'求是理论网_生态',u'生态文明','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181708%25%27&list=1181708'),
                (u'求是理论网_生态',u'能源资源','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181709%25%27&list=1181709'),
                (u'求是理论网_生态',u'环境保护','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181710%25%27&list=1181710'),
                (u'求是理论网_生态',u'绿色经济','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181711%25%27&list=1181711'),
                (u'求是理论网_生态',u'地方生态','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181712%25%27&list=1181712'),
                (u'求是理论网_生态',u'环球','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181713%25%27&list=1181713'),
                (u'求是理论网_国防',u'思想政治','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181740%25%27&list=1181740'),
                (u'求是理论网_国防',u'国防建设','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181741%25%27&list=1181741'),
                (u'求是理论网_国防',u'军事理论','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181742%25%27&list=1181742'),
                (u'求是理论网_国防',u'军情观察','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181743%25%27&list=1181743'),
                (u'求是理论网_国防',u'军营风采','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181744%25%27&list=1181744'),
                (u'求是理论网_国防',u'军史百科','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181745%25%27&list=1181745'),
                (u'求是理论网_国防',u'兵器装备','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181746%25%27&list=1181746'),
                (u'求是理论网_国际',u'中国与世界','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181755%25%27&list=1181755'),
                (u'求是理论网_国际',u'国际视点','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181756%25%27&list=1181756'),
                (u'求是理论网_国际',u'他山之石','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181757%25%27&list=1181757'),
                (u'求是理论网_国际',u'国外政党','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181758%25%27&list=1181758'),
                (u'求是理论网_国际',u'深度分析','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181759%25%27&list=1181759'),
                (u'求是理论网_国际',u'中国之声','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181760%25%27&list=1181760'),
                (u'求是理论网_国际',u'聚焦','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181762%25%27&list=1181762'),
                (u'求是理论网_国际',u'国际时评','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181764%25%27&list=1181764'),
                (u'求是理论网_国际',u'环球走笔','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181766%25%27&list=1181766'),
                (u'求是理论网_纵横',u'观点评论','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181765%25%27&list=1181765'),
                (u'求是理论网_纵横',u'互联网','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181767%25%27&list=1181767'),
                (u'求是理论网_纵横',u'港澳台侨','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181769%25%27&list=1181769'),
                (u'求是理论网_纵横',u'人物','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181771%25%27&list=1181771'),
                (u'求是理论网_纵横',u'文史','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181773%25%27&list=1181773'),
                (u'求是理论网_纵横',u'讲坛','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181775%25%27&list=1181775'),
                (u'求是理论网_纵横',u'学术','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181777%25%27&list=1181777'),
                (u'求是理论网_纵横',u'杂谈','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181778%25%27&list=1181778'),
                (u'求是理论网_纵横',u'文摘','http://www.qstheory.cn/was5/web/search?channelid=258768&prepage=40&searchword=extend5%3D%27%251181779%25%27&list=1181779'),
            ]
    def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        file_name_search=re.compile(r'\d{4}-\d{2}/\d{2}').search
        findall_list = re.compile(r"""<a.*?href=(?:'|")(.*?)(?:'|").*?>(.*?)</a>""").findall

        urls = []
        tnow = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        for feed in self.feeds:
            url = feed[2]
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
            
            lists = findall_list(content)
            for i in lists:
                m=file_name_search(i[0])
                if m:
                    pubdate = datetime.datetime.strptime(m.group(0), '%Y-%m/%d')
                else:
                    continue
                delta = tnow - pubdate
                if self.oldest_article > 0 and delta.days > self.oldest_article:
                    continue
                if r'http://' in i[0]:
                    urls.append((feed[0],'[%s]%s'%(feed[1],i[1]),i[0],None))
                else:
                    urls.append((feed[0],'[%s]%s'%(feed[1],i[1]),r'%s%s'%(r'http://www.qstheory.cn',i[0]),None))
        return urls

