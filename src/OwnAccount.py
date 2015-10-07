#!/usr/bin/python
# -*- coding: utf-8 -*-
# 当所有账号都被使用，强制使用自己账号的同学断线，自己进行登录

import os
import time
import MySQLdb

# 检查是否存在user.txt文件
if not os.path.exists('own.txt'):
    print '"own.txt" does not exist, please create one and try again :)'
    print 'Close automatically in 3 seconds.'
    time.sleep(3)
    exit(1)    # error code 1 means username or password error
# 从user.txt文件中获取授权代码
user = file('own.txt', 'r')
stuno = user.readline().strip()
user.close()

check = raw_input('Enter your password: ')

# 打开数据库连接
try:
    conn = MySQLdb.connect(host='192.168.111.72', user='root', passwd='root', db='schoolnet', port=3306)
    cur = conn.cursor()
except MySQLdb.Error, e:
    print 'MySql Error %d: %s' % (e.args[0], e.args[1])

try:
    cur.execute("SELECT phone, ip, jsessionid, online FROM accounts WHERE stuno='%s' AND pswd='%s'"%(stuno,check))
    res = cur.fetchone()
    if not res:
        print 'StudentNum or Password Error, Please correct it and try again'
        raw_input('Press enter to exit')
        exit(1)    # 学号或密码错误
    phone = res[0]
    remoteip = res[1]
    cook = res[2]
    state = int(res[3])
    if not state:
        print 'Your account was not be used. Please run Login.exe instead'
        raw_input('Press enter to exit')
        exit(1)
    print phone, remoteip, cook
    jsessionid = file('cookie.txt', 'w')
    jsessionid.write(cook + '\r\n')
    jsessionid.close()
    iprecord = file('ip.txt', 'w')
    iprecord.write(phone + '\r\n')    # 这里最好是使用提供者学号，但是为了简单直接使用提供者手机号了
    iprecord.write(remoteip)
    iprecord.close()
    # 调用前面的Logout和Login将别人踢掉然后自己登录
    os.system(os.getcwd() + '\Logout.exe')
    os.system(os.getcwd() + '\Login.exe')
    cur.close()
    conn.close()
    print 'Login Success'
except MySQLdb.Error, e:
    print 'MySql Error %d: %s' % (e.args[0], e.args[1])

