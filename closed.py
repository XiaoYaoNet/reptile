#https://github.com/bitcoin/bitcoin/issues?page=3&q=is%3Aissue+is%3Aclosed

import urllib.request
import re
from bs4 import BeautifulSoup
import io
import sys
import openpyxl

record=[]

def gettitle(page=1):
	try:
		url="https://github.com/bitcoin/bitcoin/issues?page="+str(page)+"&q=is%3Aissue+is%3Aclosed"
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
			temp.append(a[i].get_text())
			temp.append("opened")
			temp.append(c[i].attrs['datetime'])
			z=""
			for j in test[i].select('a.d-inline-block.IssueLabel.v-align-text-top'):
				z+=j.get_text()+'/'
			temp.append(z)
			#sn=b[i].get_text().replace(" ","").split('\n')[1].replace("#","").replace("\n","")
			m = re.search('\d+',b[i].get_text())
			s,t=getdata(m.group(0))
			temp.append(t)
			temp.append(s)
			record.append(temp)
		#hostsfile.close()
		#print('hosts刷新成功:',len(a))
	except Exception as err:
		print(str(err))

def getdata(sn):
	value=""
	try:
		url="https://github.com/bitcoin/bitcoin/issues/"+str(sn)
		data = urllib.request.urlopen(url).read()
		z_data = data.decode('UTF-8')
		soup = BeautifulSoup(z_data, 'lxml')
		a = soup.select('table > tbody > tr > td')
		b = soup.select('div.discussion-item.discussion-item-closed')
		#hostsfile = open('record.txt', 'w', newline='')
		for i in a:
			value=value+i.get_text()+ "\n\r"
			#hostsfile.write(value)
		#hostsfile.close()
		#print('hosts刷新成功:',len(a))
	except Exception as err:
		print(str(err))
	return value,b[0].select('relative-time')[0].attrs['datetime']

def write07Excel(path,value):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'Sheet1'
    for i in range(0, len(value)):
        for j in range(0, len(value[i])):
            sheet.cell(row=i+1, column=j+1, value=str(value[i][j]))
    wb.save(path)
    #print("写入数据成功！")

if __name__=="__main__":
	for i in range(1,24):
		try:
			gettitle(i)
			print("第"+str(i)+"页完成")
		except:
			print("第"+str(i)+"页抓取失败")
	write07Excel("closed.xlsx",record)