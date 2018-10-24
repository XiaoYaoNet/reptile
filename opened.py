import urllib.request
import re
from bs4 import BeautifulSoup
import io
import sys
import openpyxl
import xlwt
import xlrd
from xlutils.copy import copy


P=sys.argv[1]
record=[]

def write07Excel(path,value):
	wb = openpyxl.load_workbook(path)
	ws = wb['Sheet1']
	#for x in data:
	ws.append(value)
	wb.save(path)
	#print("写入成功")

def gettitle(page=1):
	try:
		url="https://github.com/bitcoin/bitcoin/issues?page="+str(page)+"&q=is%3Aissue+is%3Aopen"
		data = urllib.request.urlopen(url).read()

		z_data = data.decode('UTF-8')
		soup = BeautifulSoup(z_data, 'lxml')
		a = soup.select('li > div > div > a')
		b=soup.select('span.opened-by')
		c=soup.select('relative-time')
		test=soup.select('div.float-left.col-9.lh-condensed.p-2')

		#hostsfile = open('record.txt', 'w', newline='',encoding='UTF-8')
		for i in range(0,len(b)):
			temp=[]
			temp.append(a[i].get_text())                           #标题
			temp.append("opened")                                  #状态
			temp.append(c[i].attrs['datetime'])                    #问题提出时间
			z=""            
			for j in test[i].select('a.d-inline-block.IssueLabel.v-align-text-top'):
				z+=j.get_text()+'/'
			temp.append(z)                                         #标签
			m = re.search('\d+',b[i].get_text())
			n=m.group(0)
			temp.append(m.group(0)) #问题id    
			s=getdata(m.group(0))
			for i in s:
				temp.append(i)
			write07Excel("opened.xlsx",temp)
		print('hosts刷新成功:',len(a))
	except Exception as err:
		print(str(err))

def getdata(sn):
	temp=[]
	try:
		url="https://github.com/bitcoin/bitcoin/issues/"+str(sn)
		data = urllib.request.urlopen(url).read()
		z_data = data.decode('UTF-8')
		soup = BeautifulSoup(z_data, 'lxml')
		a = soup.select('task-lists > table > tbody > tr > td')
		#b = soup.select('div.discussion-item.discussion-item-closed')
		#author=soup.select('h3.timeline-comment-header-text.f5.text-normal > a')
		author=soup.find_all('h3',attrs={'class':'timeline-comment-header-text f5 text-normal'})
		#print(sn,len(a),len(author))
		#print(author)
		temp.append(author[0].select('a.author')[0].get_text())
		#print(sn,len(a),len(author))
		temp.append(len(a)-1)
		temp.append(a[0].get_text())
		for i in range(1,len(a)):
			tempd=[]
			tempd.append(sn)             #问题id
			tempd.append(author[i].select('a.author')[0].get_text()) #评论人id
			tempd.append(author[i].select('relative-time')[0].attrs['datetime'])                      #评论时间
			tempd.append(a[i].get_text())                                                           #评论内容
			write07Excel("opened_comment.xlsx",tempd)	
		return temp
		
	except Exception as err:
		print(str(err))
	'''
	if len(b[0].select('relative-time'))>0:
		return temp,b[0].select('relative-time')[0].attrs['datetime']
	else:
		return temp,""
	'''

if __name__=="__main__":
	#for i in range(1,25):
		try:
			gettitle(float(P))
			print("第"+str(P)+"页完成")
		except Exception as err:
			hostsfile = open('record.txt', 'w', newline='')
			hostsfile.write(str(P)+":"+str(err) + "\n")
			hostsfile.close()
			#print("第"+str(i)+"页抓取失败")
	#write07Excel("closed.xlsx",record)