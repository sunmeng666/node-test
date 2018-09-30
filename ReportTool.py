#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-  

import requests
from html.parser import HTMLParser
from lxml import etree
import time
import csv
from itertools import islice
import smtplib
from email.mime.text import MIMEText
from email.header import Header


# redmine object---
class RedmineClient(object):
	def __init__(self):
		object.__init__(self)
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
		      "Host": "redmine.uisee.ai",
		      "Connection": "keep-alive",
		      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		      "Referer": "https://redmine.uisee.ai/",
		      "Upgrade-Insecure-Requests": "1"
		      }
		self.session = requests.Session()
		self.session.headers.update(headers)
		self.token = get_authenticity_token(self.session.get('https://redmine.uisee.ai/').text)
		self.bugList = []

	def login_redmine(self):
		data = {
			"utf8": "✓",
			"authenticity_token": self.token,
			"back_url": "https://redmine.uisee.ai/",
			"username": "luxx",
			"password": "123456",
			"login": "Login"
			}
		url = "https://redmine.uisee.ai/login"
		self.session.post(url, data=data)

	def download_buglist(self):
		url = "https://redmine.uisee.ai/issues.csv"
		params = {
				"utf8": "✓",
				"set_filter": "1",
				"sort": "id:desc",
				"f[]": ["status_id","cf_15"],
				"op[status_id]": "o",
				"op[cf_15]": "=",
				"v[cf_15][]": "常青（基于ARM）",
				# "op[created_on]": "lm"
				"c[]": ["tracker","project","status","priority","subject","assigned_to","updated_on","tracker",""],
			    "t[]": ""
				}
		csv_file = self.session.get(url,params=params).content
		with open("bug.csv", "wb") as code:
			code.write(csv_file)

def _attr(attrs,attrName):
	for attr in attrs:
		if attr[0] == attrName:
			return attr[1]

def get_authenticity_token(content):
	class RedmineParser(HTMLParser):
		"""docstring for MovieParser"""
		def __init__(self):
			HTMLParser.__init__(self)
			self.authenticity_token = None

		def handle_starttag(self, tag, attrs):
			if tag == 'input' and _attr(attrs, 'type') == "hidden" and _attr(attrs, 'name') == "authenticity_token":
				self.authenticity_token = _attr(attrs, 'value')
	redmineParser = RedmineParser()
	redmineParser.feed(content)
	return redmineParser.authenticity_token

def getBugCount():
	bugCount = {}
	nameList = []
	with open("bug.csv","r") as f:
		readLine = islice(csv.reader(f,delimiter=','),1,None)
		# print(readLine)
		for row in readLine:
			if row[4] == "Urgent":
				if row[-2] in bugCount.keys():
					bugCount[row[-2]] = bugCount[row[-2]] + 1
				else:
					bugCount[row[-2]] = 1
					nameList.append(row[-2])
	return nameList,bugCount

def htmlCode():

	nameList,bugCount = getBugCount()
	list1 = []
	for i in nameList:
		list1.append((i,bugCount[i]))

	letter = """
	                <table color="CCCC33" width="800" border="1" cellspacing="0" cellpadding="5" text-align="center">

	                        <tr>

	                                <th text-align="center">name</th>

	                                <th text-align="center">UrgentCount</th>

	                        </tr>   
	        """

	for thelist in list1:

		text = '''
	                        <tr>   

	                                <td style="text-align: center">%s </td>

	                                <td style="text-align: center">%s </td>


	                        </tr>
		        ''' % (thelist)
		letter = letter + text
	return letter


def autoSendMail():
	mail_host="smtp.uisee.com"  #设置服务器
	mail_user="lux.xiao@uisee.com"    #用户名
	mail_pass="123456"   #口令 
	 
	sender = 'lux.xiao@uisee.com'
	receivers = 'lux.xiao@uisee.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
	letter = htmlCode()
	message = MIMEText(letter, 'HTML', 'utf-8')

	message['From'] = Header("AutoReport",'utf-8')
	message['To'] =  Header("test1", 'utf-8')
	 
	subject = '【常青】未关闭问题统计'
	message['Subject'] = Header(subject, 'utf-8')
 
	try:
	    smtpObj = smtplib.SMTP() 
	    smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
	    smtpObj.login(mail_user,mail_pass)
	    smtpObj.sendmail(sender, receivers, message.as_string())
	    print ("suce")
	except smtplib.SMTPException:
	    print ("Error: ")


rc = RedmineClient()

rc.login_redmine()
rc.download_buglist()
autoSendMail()