#-*- coding:utf-8 -*-

import requests
from lxml import etree
import time
import os

session = requests.session()  #同.Session()

init_url = 'https://www.zhihu.com/#signin'
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
}
#response1 = requests.get(url1,headers= headers)# 这里需要加上headers，不然会报500错误

def get_xsrf():
	""" 获得_xsrf
	"""
	response1 = session.get(init_url, headers = headers)
	try:
		html = etree.HTML(response1.content)# 通过etree解析页面
		print('*'*20)
	except:
		print('the error requests')

	_xsrf = html.xpath('//input[@name="_xsrf"]/@value')[0]
	print('获得xsrf')
	return _xsrf

def get_captcha():
	"""获取验证码图片
	"""
	points = [[20.2969,26],[45.2969,26],[68.2969,26],\
	         [92.2969,24],[118.297,25],[145.297,23],[172.297,22]]
	#captcha_url = 'https://www.zhihu.com/captcha.gif?'+\
	#str(int(time.time()*1000))+'&amp'
	captcha_url = 'https://www.zhihu.com/captcha.gif?r='+str(int(time.time()*1000))+'&type=login&lang=cn'
	data = {'captcha_type':'cn'}
	try:
		response2 = session.get(captcha_url, data = data, headers= headers)
		print('成功获得验证码图片')
	except:
		print('获得验证码失败')
	#response2 = session.get(captcha_url,data = data, headers= headers)
	#print('获得验证码图片')
	with open('captcha.gif','wb') as f:
		f.write(response2.content)
	os.startfile('captcha.gif')
	a = input('请输入倒立字的位置：')
	pp =''
	for i in a:
		pp += str(points[int(i)-1])+','
		print(pp)
	if pp:
		yanzhengma = '{"img_size":[200,44],"input_points":[%s]}' %pp[:-1]
		print(yanzhengma)
		return yanzhengma
	else:
		return 0

def log_in():
	"""登录知乎
	"""
	log_in_url = 'https://www.zhihu.com/login/phone_num'
	phonenum = input('请输入手机号: ')
	password = input('请输入密码：')
	headers['referer'] = 'https://www.zhihu.com/'
	a = get_xsrf()
	#print(a)
	b = get_captcha()
	#print(b)
	post_data = {
	'phone_num': phonenum, 'password': password, 'captcha_type':'cn','_xsrf': a, 'captcha': b
	}
	response3 = session.post(log_in_url,data = post_data, headers = headers)
	print(response3.status_code)

def print_sth():
	"""获取登陆后的页面内容，没有登陆时会跳转到登陆页面
	"""
	url = 'https://www.zhihu.com/people/zhong-yuan-29-90/logs'
	response4 = session.get(url,headers= headers)
	print(response4.url) #没登陆时会跳转到‘https://www.zhihu.com/?next=%2Fpeople%2Fzhong-yuan-29-90%2Flogs’
	html = etree.HTML(response4.text)
	result = etree.tostring(html)
	print(result)
	print(type(result))
	print('*'*20)
	#print(result.decode('utf-8'))
	#print(html)
	with open('zhihu123.html','w') as f:
		f.write(result.decode('utf-8'))

if __name__ == "__main__":
	#get_captcha()
	#log_in()
	print_sth()
