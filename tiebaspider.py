'''
贴吧发言爬虫
'''
import requests
import os
import urllib
from urllib import request
from bs4 import BeautifulSoup
from retrying import retry
import xlwt
import lxml

@retry(stop_max_attempt_number=3)
def souping(url):
	global timeouttag
	headers = {
		"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
		"Referer": "https://www.cnblogs.com"
	}
	try:
		src = requests.get(url, headers=headers,timeout=20).content
		soup=BeautifulSoup(src,"lxml").decode("gbk")
		soup=BeautifulSoup(soup,"lxml")
		return soup
	except:
		print("超时")
		timeouttag=1
		pass
def foruming(soup):
	global textnum
	ctextnum=textnum
	text_base = soup.find_all(class_="s_post")
	for text_content in text_base:
		t=text_content.find(class_="p_forum")
		try:
			worksheet.write(ctextnum,0,t.text)
			ctextnum = ctextnum + 1
		except:
			pass
def authoring(soup):
	global textnum
	ctextnum=textnum
	text_base = soup.find_all(class_="s_post")
	for text_content in text_base:
		t=text_content.find_all("font",class_="p_violet")
		try:
			worksheet.write(ctextnum,1,t[1].text)
			ctextnum=ctextnum+1
		except:
			pass
def titling(soup):
	global textnum
	ctextnum=textnum
	text_base = soup.find_all(class_="s_post")
	for text_content in text_base:
		t=text_content.find(class_="p_title")
		try:
			worksheet.write(ctextnum,2,t.text)
			ctextnum = ctextnum + 1
		except:
			pass
def contenting(soup):
	global textnum
	ctextnum=textnum
	text_base = soup.find_all(class_="s_post")
	for text_content in text_base:
		t=text_content.find(class_="p_content")
		try:
			worksheet.write(ctextnum,3,t.text)
			ctextnum = ctextnum + 1
		except:
			pass
def timing(soup):
	global textnum
	ctextnum=textnum
	text_base = soup.find_all(class_="s_post")
	for text_content in text_base:
		t=text_content.find(class_="p_green p_date")
		try:
			worksheet.write(ctextnum,4,t.text)
			ctextnum = ctextnum + 1
		except:
			pass
	textnum = ctextnum


if __name__=="__main__":
	now_pages=1
	textnum=1
	timeouttag=0
	required_pages = input("请输入要爬取的页数：")
	while isinstance(required_pages,int)|int(required_pages)<=0:
		required_pages=input("请输入正整数！请重新输入要爬取的页数")
	print("正在创建excel表格……")
	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet("sheet1")
	worksheet.write(0, 0, "贴吧")
	worksheet.write(0, 1, "作者")
	worksheet.write(0, 2, "标题")
	worksheet.write(0, 3, "发言")
	worksheet.write(0, 4, "时间")
	workbook.save("贴吧发言列表.xls")
	url = "http://tieba.baidu.com/f/search/ures?kw=&qw=&rn=10&un=%C9%F1%B7%E7%E9%A3%D3%A5&only_thread=&sm=5&sd=&ed=&pn=" + str(now_pages)
	soup=souping(url)
	print("开始爬取……")
	while now_pages <= int(required_pages):
		try:
			print("现在正在爬取第" + str(now_pages) + "页，已保存" + str(textnum) + "条发言")
			if timeouttag==0:
				foruming(soup)
				authoring(soup)
				titling(soup)
				contenting(soup)
				timing(soup)
			now_pages=now_pages+1
			timeouttag=0
			url="http://tieba.baidu.com/f/search/ures?kw=&qw=&rn=10&un=%C9%F1%B7%E7%E9%A3%D3%A5&only_thread=&sm=5&sd=&ed=&pn=" + str(now_pages)
			print("爬取的链接是："+url)
			soup=souping(url)
		except:
			print("爬取失败")
			exit()
			pass
		workbook.save("贴吧发言列表.xls")
	print("爬取完成～")



