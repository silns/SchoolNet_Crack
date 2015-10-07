#!/usr/bin/python
# -*- coding: utf-8 -*-
# 模拟网页退出

import urllib
import httplib2
import re
import os
import MySQLdb

# 检查是否已登录
if not os.path.exists('cookie.txt'):
    print 'You didn\'t login yet :)'
    raw_input('Press enter to exit')
    exit(1)  # error code 1 means not login

encodeUrl = '+++%B6%CF%CF%DF++++'
decodeUrl = urllib.unquote(encodeUrl)

logoutUrl = 'http://121.33.233.154/portalDisconnAction.do'
h = httplib2.Http()
# 获取JSESSIONID
jsessionid = file('cookie.txt', 'r')
cook = jsessionid.readline()
jsessionid.close()
# 获取phone和本机ip
ipinfo = file('ip.txt')
phone = ipinfo.readline().strip()
ip = ipinfo.readline().strip()
ipinfo.close()

postData = {
    'wlanuserip':ip,
    'wlanacname':'hssfxy-SR6604',
    'portalUrl':'http://',
    'wlanacIp':'125.91.232.98',
    'disconnect':decodeUrl
}
postData = urllib.urlencode(postData)

headers = {
    'Accept':'text/html, application/xhtml+xml, */*',
    'Referer':'http://121.33.233.154/portalAuthAction.do',
    'Accept-Language':'zh-CN',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Content-Type':'application/x-www-form-urlencoded',
    'Accept-Encoding':'gzip, deflate',
    'Host':'121.33.233.154',
    'Content-Length':'142',
    'Connection':'Keep-Alive',
    'Cache-Control':'no-cache',
    'Cookie':cook
}

resp, content = h.request(logoutUrl, method='POST', headers=headers, body=postData)
content = content.decode('gbk').encode('utf8')

m = re.search('下线成功', content)
if m:
    # 下线成功，则删除暂存文件，更新数据库
    print 'Logout Success'
    os.remove('cookie.txt')
    os.remove('ip.txt')
    try:
        conn = MySQLdb.connect(host='192.168.111.72', user='root', passwd='root', db='schoolnet', port=3306)
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET online='%s' WHERE phone='%s'"%('0', phone))
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print 'MySql Error %d: %s' % (e.args[0], e.args[1])
else:
    print 'Logout Failed'
    raw_input('Press enter to exit')

