#!/usr/bin/env python
# -*- coding:utf-8 -*-
#A GAE web application to aggregate rss and send it to your kindle.
#Visit https://github.com/cdhigh/KindleEar for the latest version
#中文讨论贴：http://www.hi-pda.com/forum/viewthread.php?tid=1213082
#Author:
# cdhigh <https://github.com/cdhigh>
#Contributors:
# rexdf <https://github.com/rexdf>

import os, datetime, logging, __builtin__, hashlib, time

import web
import jinja2
from utils import *
from config import *
from apps.dbModels import *
from google.appengine.api import mail
from google.appengine.api.mail_errors import (InvalidSenderError,
                                           InvalidAttachmentTypeError)
from google.appengine.runtime.apiproxy_errors import (OverQuotaError,
                                                DeadlineExceededError)

#import main

class BaseHandler:
    " URL请求处理类的基类，实现一些共同的工具函数 "
    def __init__(self):
        if not main.session.get('lang'):
            main.session.lang = self.browerlang()
        set_lang(main.session.lang)
        
    @classmethod
    def logined(self):
        return True if main.session.get('login') == 1 else False
    
    @classmethod
    def login_required(self, username=None):
        if (main.session.get('login') != 1) or (username and username != main.session.get('username')):
            raise web.seeother(r'/login')
    
    @classmethod
    def getcurrentuser(self):
        self.login_required()
        u = KeUser.all().filter("name = ", main.session.username).get()
        if not u:
            raise web.seeother(r'/login')
        return u
        
    def browerlang(self):
        lang = web.ctx.env.get('HTTP_ACCEPT_LANGUAGE', "en")
        #分析浏览器支持那些语种，为了效率考虑就不用全功能的分析语种和排序了
        #此字符串类似：zh-cn,en;q=0.8,ko;q=0.5,zh-tw;q=0.3
        langs = lang.lower().replace(';',',').replace('_', '-').split(',')
        langs = [c.strip() for c in langs if '=' not in c]
        baselangs = {c.split('-')[0] for c in langs if '-' in c}
        langs.extend(baselangs)
        
        for c in langs: #浏览器直接支持的语种
            if c in main.supported_languages:
                return c
        for c in langs: #同一语种的其他可选语言
            for sl in main.supported_languages:
                if sl.startswith(c):
                    return sl
        return main.supported_languages[0]
        
    @classmethod
    def deliverlog(self, name, to, book, size, status='ok', tz=TIMEZONE):
        if type(to) == list:
            to = ';'.join(to)
        try:
            dl = DeliverLog(username=name, to=to, size=size,
               time=local_time(tz=tz), datetime=datetime.datetime.utcnow(),
               book=book, status=status)
            dl.put()
        except Exception as e:
            default_log.warn('DeliverLog failed to save:%s',str(e))
    
    @classmethod
    def SendToKindle(self, name, to, title, booktype, attachment, tz=TIMEZONE, filewithtime=True):
        if PINYIN_FILENAME: # 将中文文件名转换为拼音
            from calibre.ebooks.unihandecode.unidecoder import Unidecoder
            decoder = Unidecoder()
            basename = decoder.decode(title)
        else:
            basename = title
            
        lctime = local_time('%Y-%m-%d_%H-%M',tz)
        if booktype:
            if filewithtime:
                filename = "%s(%s).%s"%(basename,lctime,booktype)
            else:
                filename = "%s.%s"%(basename,booktype)
        else:
            filename = basename
            
        for i in range(SENDMAIL_RETRY_CNT+1):
            try:
                if ";" in to:
                    to = to.split(";")
                mail.send_mail(SRC_EMAIL, SRC_EMAIL, "News Feeds %s" % lctime, "Deliver from News Feeds",
                    attachments=[(filename, attachment),],bcc = to)    
                # mail.send_mail(SRC_EMAIL, to, "News Feeds %s" % lctime, "Deliver from News Feeds",
                #     attachments=[(filename, attachment),])
                # mail.send_mail(SRC_EMAIL, to, "News Feeds %s" % lctime, "Deliver from News Feeds",
                #     attachments=[(filename, attachment),])
                # mail.send_mail(sender = SRC_EMAIL, bcc = to,subject = "News Feeds %s" % lctime, body = "Deliver from News Feeds",
                #     attachments=[(filename, attachment),])
            except OverQuotaError as e:
                default_log.warn('overquota when sendmail to %s:%s' % (to, str(e)))
                self.deliverlog(name, to, title, len(attachment), tz=tz, status='over quota')
                default_log.warn('overquota when sendmail to %s:%s, retry!' % (to, str(e)))
                time.sleep(10)
                if i>2:
                    break
            except InvalidSenderError as e:
                default_log.warn('UNAUTHORIZED_SENDER when sendmail to %s:%s' % (to, str(e)))
                self.deliverlog(name, to, title, len(attachment), tz=tz, status='wrong SRC_EMAIL')
                break
            except InvalidAttachmentTypeError as e: #继续发送一次
                if SENDMAIL_ALL_POSTFIX:
                    filename = filename.replace('.', '_')
                    title = title.replace('.', '_')
                else:
                    default_log.warn('InvalidAttachmentTypeError when sendmail to %s:%s' % (to, str(e)))
                    self.deliverlog(name, to, title, len(attachment), tz=tz, status='invalid postfix')
                    break
            except DeadlineExceededError as e:
                if i < SENDMAIL_RETRY_CNT:
                    default_log.warn('timeout when sendmail to %s:%s, retry!' % (to, str(e)))
                    time.sleep(5)
                else:
                    default_log.warn('timeout when sendmail to %s:%s, abort!' % (to, str(e)))
                    self.deliverlog(name, to, title, len(attachment), tz=tz, status='timeout')
                    break
            except Exception as e:
                default_log.warn('sendmail to %s failed:%s.<%s>' % (to, str(e), type(e)))
                self.deliverlog(name, to, title, len(attachment), tz=tz, status='send failed')
                break
            else:
                self.deliverlog(name, to, title, len(attachment), tz=tz)
                break
    
    @classmethod
    def SendHtmlMail(self, name, to, title, html, attachments, tz=TIMEZONE):
        for i in range(SENDMAIL_RETRY_CNT+1):
            try:
                if attachments:
                    if ";" in to:
                        to = to.split(";")
                    mail.send_mail(SRC_EMAIL, to, title, "Deliver from News Feeds, refers to html part.",
                        html=html, attachments=attachments)
                else:
                    if ";" in to:
                        to = to.split(";")
                    mail.send_mail(SRC_EMAIL, to, title, "Deliver from News Feeds, refers to html part.",
                        html=html)
            except OverQuotaError as e:
                default_log.warn('overquota when sendmail to %s:%s' % (to, str(e)))
                self.deliverlog(name, to, title, 0, tz=tz, status='over quota')
                break
            except InvalidSenderError as e:
                default_log.warn('UNAUTHORIZED_SENDER when sendmail to %s:%s' % (to, str(e)))
                self.deliverlog(name, to, title, 0, tz=tz, status='wrong SRC_EMAIL')
                break
            except InvalidAttachmentTypeError as e:
                default_log.warn('InvalidAttachmentTypeError when sendmail to %s:%s' % (to, str(e)))
                self.deliverlog(name, to, title, 0, tz=tz, status='invalid postfix')
                break
            except DeadlineExceededError as e:
                if i < SENDMAIL_RETRY_CNT:
                    default_log.warn('timeout when sendmail to %s:%s, retry!' % (to, str(e)))
                    time.sleep(5)
                else:
                    default_log.warn('timeout when sendmail to %s:%s, abort!' % (to, str(e)))
                    self.deliverlog(name, to, title, 0, tz=tz, status='timeout')
                    break
            except Exception as e:
                default_log.warn('sendmail to %s failed:%s.<%s>' % (to, str(e), type(e)))
                self.deliverlog(name, to, title, 0, tz=tz, status='send failed')
                break
            else:
                if attachments:
                    size = len(html) + sum([len(c) for f,c in attachments])
                else:
                    size = len(html)
                self.deliverlog(name, to, title, size, tz=tz)
                break
    
    def render(self, templatefile, title='PartyNews', **kwargs):
        kwargs.setdefault('nickname', main.session.get('username'))
        kwargs.setdefault('lang', main.session.get('lang', 'en'))
        kwargs.setdefault('version', main.__Version__)
        return main.jjenv.get_template(templatefile).render(title=title, **kwargs)