![SNCrack](https://github.com/silns/SchoolNet_Crack/blob/master/head.jpg)

鉴于学校电信月租贵、寒暑假不能停用、网络共享240分钟的情况，我写了这样一个工具，可以收集很多账号，然后提供账号的人没用时其他人可以暂时使用他们的账号来上网

## 功能介绍
1. Login实现自动登录
2. Logout实现自动退出
3. OwnAccount强制使用自己账号的同学退线自己登录
4. ShareAccount把自己的账号共享到服务器数据库中

## 特点
1. 操作简单，只需要双击
2. 方便，随时可以登录、退出登录
3. 不需要一直开着浏览器暂用系统资源

## 运行环境
* Python2.7
* httplib2
* MySQLDB-python
* py2exe
* VCForPython27（可能需要，看电脑环境而定）


## 安装说明
1. 安装Python2.7
2. 安装httplib2、MySQLDB-python、py2exe、VCForPython27这几个依赖库
	* pip install httplib2
	* pip install MySQLDB-python
	* pip install py2exe
	* ...
	* 如果没法直接使用pip安装则到百度下载相关exe包进行安装
3. 将源文件编译成exe可执行文件（假如工作目录为D:\SchoolNet）
	* 打开“命令提示符”，使用cd命令切换到D:\SchoolNet文件夹（cd D:\SchoolNet)
	* 编写build.py，仓库有提供
	* 运行build.py进行编译（python build.py py2exe）
4. 数据库
	* 安装MySQL数据库
	* 建立数据库（CREATE DATABASE schoolnet）
	* 建立数据表及插入数据（直接运行提供的table.sql即可）
