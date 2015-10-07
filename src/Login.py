#!/usr/bin/python
# -*- coding: utf-8 -*-
# 模拟网页登录

import urllib
import httplib2
import subprocess
import socket
import re
import os
import time
import MySQLdb
# 初始化变量（可以去掉）
access = 0
logined = 0
stuno = ''
userid = ''
passwd = ''
m = ''

# 检查是否存在user.txt文件
if not os.path.exists('user.txt'):
    print '"user.txt" does not exist, please create one and try again :)'
    raw_input('Press enter to exit')
    exit(1)    # error code 1 means username or password error
# 从user.txt文件中获取授权代码
user = file('user.txt', 'r')
stuno = user.readline().strip()
user.close()

# 打开数据库连接
try:
    conn = MySQLdb.connect(host='192.168.111.72', user='root', passwd='root', db='schoolnet', port=3306)
    cur = conn.cursor()
except MySQLdb.Error, e:
    print 'MySql Error %d: %s' % (e.args[0], e.args[1])

try:
    # 查看该授权代码是否有效
    cur.execute("SELECT COUNT(stuno) FROM students WHERE stuno='%s'"%(stuno,))
    res = cur.fetchone()
    access =  int(res[0])
    if not access:
        print 'You have no access to connect'
        cur.close()
        conn.close()
        raw_input('Press enter to exit')
        exit(2)    # error code 2 means have no access
except MySQLdb.Error, e:
    print 'MySql Error %d: %s' % (e.args[0], e.args[1])

while not logined:
    try:
        # 检查并获取一个空闲用户的账号和密码
        cur.execute("SELECT phone, pswd FROM accounts WHERE online='%s'"%('0',))
        res = cur.fetchone()
        if not res:
            print 'No available account for you :)'
            cur.close()
            conn.close()
            raw_input('Press enter to exit')
            exit(3)    # error code 3 means no available account
        userid = res[0]
        passwd = res[1]
    except MySQLdb.Error, e:
        print 'MySql Error %d: %s' % (e.args[0], e.args[1])

    # 查看本地所有启用ip地址
    res = subprocess.Popen(['ipconfig'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, err_msg = res.communicate()
    #print output.decode('gbk').encode('utf-8')

    # 选择进行连接的ip地址
    localIp = socket.gethostbyname_ex(socket.gethostname())
    ips = len(localIp[2])
    ip = localIp[2][0]
    if ips < 0:
        print 'No ip found in you computer'
        raw_input('Press enter to exit')
        exit(4)    # error code 4 means ip not found
    elif ips > 1:
        print 'Please select the right network :)'
        for i in range(0, ips):
            print i,'-',localIp[2][i]
        sel = int(raw_input('select your network: '))
        ip = localIp[2][sel]
    #print ip

    loginUrl = 'http://121.33.233.154/portalAuthAction.do'
    h = httplib2.Http('.cache')
    postData = {
        'wlanuserip':ip,
        'wlanacname':'hssfxy-SR6604',
        'chal_id':'',
        'chal_vector':'',
        'auth_type':'PAP',
        'seq_id':'',
        'req_id':'',
        'wlanacIp':'125.91.232.98',
        'service':'internet',
        'userid':userid,
        'passwd':passwd
    }
    postData = urllib.urlencode(postData)

    headers = {
        'Host':'121.33.233.154',
        'Connection':'Keep-Alive',
        'Accept':'text/html, application/xhtml+xml, */*',
        'Referer':'http://121.33.233.154/portalReceiveAction.do?wlanacname=hssfxy-SR6604&wlanuserip=192.168.111.72',
        'Accept-Language':'zh-CN',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept-Encoding':'gzip, deflate',
        'Cache-Control':'no-cache',
        'service':'internet'
    }

    resp, content = h.request(loginUrl, method='POST', headers=headers, body=postData)
    content = content.decode('gbk').encode('utf8')

    # 将密码错误的账号从数据库中移除
    m = re.search('密码错误', content)
    if m:
        cur.execute("DELETE FROM accounts WHERE phone='%s'"%(userid,))
        conn.commit()
    else:
        logined = 1

m = re.search('可用天数为', content)
if m:
    print 'Login Success'
    cook = resp['set-cookie']
    cook = cook[0:cook.index(';')]
    jsessionid = file('cookie.txt', 'w')
    jsessionid.write(cook + '\r\n')
    jsessionid.close()
    iprecord = file('ip.txt', 'w')
    iprecord.write(userid + '\r\n')    # 这里最好是使用提供者学号，但是为了简单直接使用提供者手机号了
    iprecord.write(ip)
    iprecord.close()
    try:
        cur.execute("UPDATE accounts SET ip='%s', online='%s', jsessionid='%s' WHERE phone='%s'"%(ip,'1',cook,userid))
        conn.commit()
        cur.execute("INSERT INTO history VALUES('%s','%s','%s','%s')"%(stuno, userid, time.strftime('%Y-%m-%d %X', time.localtime(time.time())), ip))
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print 'MySql Error %d: %s' % (e.args[0], e.args[1])
else:
    print 'Login Failed'
    raw_input('Press enter to exit')

