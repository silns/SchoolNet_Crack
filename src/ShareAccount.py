#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import MySQLdb

# 打开数据库连接
try:
    conn = MySQLdb.connect(host='192.168.111.72', user='root', passwd='root', db='schoolnet', port=3306, charset="utf8")
    cur = conn.cursor()
except MySQLdb.Error, e:
    print 'MySql Error %d: %s' % (e.args[0], e.args[1])

print 'Insert you informations'
check = 0
# 输入信息直到确认无误确定
while not check:
    stuno = raw_input('StudentNumber: ')
    name = raw_input('Name: ')
    name = name.decode('gbk').encode('utf-8')
    phone = raw_input('PhoneNumber: ')
    pswd = raw_input('Password: ')
    os.system('cls')
    print 'Your information is: '
    print 'StudentNumber:', stuno
    print 'Name:', name.decode('utf-8').encode('gbk')
    print 'Phone:', phone
    print 'Password:', pswd
    check = raw_input('Input 0 to cancel, 1 to submit, 2 to quit: ')
    check = int(check)
    if check == 2:
        exit(1)

try:
    # 检查并获取一个空闲用户的账号和密码
    cur.execute("INSERT INTO accounts VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(stuno, name, phone, pswd, '0', '', ''))
    cur.execute("INSERT INTO students VALUES('%s', '%s')"%(stuno, name))
    conn.commit()
    cur.close()
    conn.close()
    print 'Share OK'
    raw_input('Press any key to exit')
except MySQLdb.Error, e:
    print 'MySql Error %d: %s' % (e.args[0], e.args[1])
