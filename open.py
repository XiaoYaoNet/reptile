#https://github.com/bitcoin/bitcoin/issues?page=1&q=is%3Aopen+is%3Aissue

import urllib.request
import re
from bs4 import BeautifulSoup
import io
import sys
import openpyxl

record=[]

def gettitle(page=1):
	try:
		#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='UTF-8')
		url="https://github.com/bitcoin/bitcoin/issues?page="+str(page)+"&q=is%3Aopen+is%3Aissue"
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
			temp.append(getdata(m.group(0)))
			record.append(temp)
		#hostsfile.close()
		print('hosts刷新成功:',len(a))
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
		#hostsfile = open('record.txt', 'w', newline='')
		for i in a:
			value=value+i.get_text()+ "\n\r"
			#hostsfile.write(value)
		#hostsfile.close()
		#print('hosts刷新成功:',len(a))
	except Exception as err:
		print(str(err))
	return value

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
		gettitle(i)
		print("第"+str(i)+"页抓取完成")
	write07Excel("open.xlsx",record)