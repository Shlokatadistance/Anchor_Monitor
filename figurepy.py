#scrape graph data
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import matplotlib.pyplot as plt
import csv
import json
import matplotlib.dates as md
import mpld3
from mpld3 import plugins
from datetime import datetime
import matplotlib.dates as mdates


"""
path = '/Users/singularity/Hex/chromedriver'
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(path,options=op)
url = 'https://app.anchorprotocol.com/'
driver.get(url)
time.sleep(4.5)
page = driver.page_source

soup = BeautifulSoup(page,'html.parser')
predicate = {'class':re.compile( '.*stablecoin*.')}
content = soup.find(**predicate)
	#print(content)
c_1 = content.find('div',attrs={'class':'NeuSection-content'})
c_2 = c_1.find('figure')
c_3 = c_2.find_all('div')
print(c_3)

"""

"""
r = requests.get("https://api.anchorprotocol.com/api/v1/deposit")
#print(r.text)

r_1 = requests.get("https://api.anchorprotocol.com/api/v1/deposit/1d")
#print(r_1.text)
x = r_1.json()
#print(x)
#print(len(x['total_ust_deposits']))
list_0 = []
list_0_1 = []
print(x)
for i in x['total_ust_deposits']:
	print(i)
	list_0.append(float(i['deposit']))
	list_0_1.append(float(i['timestamp']))
plt.plot(list_0_1, list_0)
plt.show()
#print(x['total_ust_deposits'][0])

#print(r_1.json())
#print(r_1.text.split(','))

r_2  = requests.get("https://api.anchorprotocol.com/api/v1/borrow/1d")
#print(r_2.text)
#print(r_2.json())
list_1 = []
list_2 = []
y = r_2.json()
print(len(y))
for i in y:
	print(i)
	list_1.append(float(i['total_borrowed']))
	list_2.append(float(i['timestamp']))

plt.plot(list_2,list_1)
plt.show()
"""
def set_size(w,h, ax=None):
    """ w, h: width, height in inches """
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)

def get_graphs():
	r_1 = requests.get("https://api.anchorprotocol.com/api/v1/deposit/1d")
	r_2  = requests.get("https://api.anchorprotocol.com/api/v1/borrow/1d")

	x = r_1.json()
	list_0 = []
	list_0_1 = []
	list_9 = []
	#print(x)
	for i in x['total_ust_deposits']:
		#print(i)
		list_0.append(float(i['deposit']))
		list_0_1.append(float(i['timestamp']))
		list_9.append(datetime.fromtimestamp(i['timestamp']//1000).strftime('%Y-%m-%d'))
	#print(list_9[::-1])
	list_1 = []
	list_2 = []
	y = r_2.json()
	for i in y:
		#print(i)
		#i['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['timestamp']))
		list_1.append(float(i['total_borrowed']))
		list_2.append(float(i['timestamp']))
	fig,ax = plt.subplots()
	#xticks = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	#ax.set(xticks=x, xticklabels=xticks)
	xticks= []
	for i in list_2:
		x = datetime.fromtimestamp(i/1000).strftime('%m%d')
		#print(x.month)
		xticks.append(x)
		#print(x)
	#print(xticks)
	#plt.xticks(xticks)
	#ax.set(xticks=x, xticklabels=xticks)
	#print(list_9[::-1])

	#ax.plot(list_9[::-1],list_0[::-1])
	#ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
	#ax.set_title('fig.autofmt_xdate fixes the labels')
	#fig.autofmt_xdate()
	ax.plot(list_2,list_1,'r',label='Borrow')
	ax.plot(list_0_1,list_0,'g',label='Deposit')
	plt.show()
	labels = [item.get_text() for item in ax.get_xticklabels()]
	print(labels)
	for i in range(len(labels)):
		print(labels[i])
		labels[i] = datetime.fromtimestamp(float(labels[i])).strftime('%Y-%m-%d')
	xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
	ax.set_xlabel('TimeStamps')
	ax.set_ylabel('Prices(in million UST)')
	ax.set_title('Deposits vs Borrow [StableCoin Market]')
	set_size(20,20)
	#ax.xaxis.set_major_formatter(xfmt)
	ax.legend()
	#plt.show()
	plt.savefig('graph.png')

	"""
	handles, labels = ax.get_legend_handles_labels() # return lines and labels
	interactive_legend = plugins.InteractiveLegendPlugin(zip(handles,
                                                         ax.collections),
                                                     labels,
                                                     alpha_unsel=0.5,
                                                     alpha_over=1.5, 
                                                     start_visible=True)
	plugins.connect(fig, interactive_legend)

	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_title('Deposits vs Borrow [StableCoin Market]', size=20)
	plt.show()	#return HttpResponse(g)
	"""




	#plt.plot(list_2, list_1,'r')
	#plt.plot(list_0_1,list_0,'g')
	#plt.show()
get_graphs()
def total_circulation(page):
	soup = BeautifulSoup(page,'html.parser')
	content_0 = soup.find('div',attrs={'class':'NeuSection-content'})
	print(type(content_0))
	content_1 = content_0.find('p',attrs={'class':'amount'})
	content_2 = content_0.find_all('section')
	content_3 = content_0.find('figure')
	content_3_1 = content_3.find_all('div')
	content_3_2 = content_3_1[1].find_all('p')
	total_deposit = content_3_2[0].find('span')
	total_collateral = content_3_2[1].find('span')
	yield_reserve = content_2[1].find('span')
	total_value_locked = content_1.find('span')
	#print("Total Value locked is ",total_value_locked.text)
	#print("Total Yield reserve is",yield_reserve.text)
	#print("Total Collateral is",total_collateral.text)
	#print("Total Deposit is",total_deposit.text)
	dict_1 = {'Total_Value_locked':total_value_locked.text,
	'Total_Yield_reserve':yield_reserve.text,
	'Total_Collateral': total_collateral.text,
	'Total_Deposit': total_deposit.text
	}

	#with open('total_circulation.csv','w') as f:
	#	for key in dict_1.keys():
	#		f.write("%s, %s\n" % (key,dict_1[key]))

	return dict_1


def keep_refreshing_anchor():
	while True:

		start_time = time.time()
		path = '/Users/singularity/Hex/chromedriver'
		op = webdriver.ChromeOptions()
		op.add_argument('headless')
		driver = webdriver.Chrome(path,options=op)
		url = 'https://app.anchorprotocol.com/'
		driver.get(url)
		time.sleep(4.5)
		page = driver.page_source
	#soup = BeautifulSoup(page,'html.parser')
	#print(soup)

		driver.quit()
		x_1 = total_circulation(page)
	#x_2 = ANC_stats(page)
	#x_3 = buyback_stats(page)
	#x_4 = stablecoin_market(page)
	#x_5 = bonded_prices(page)
	#x_6 = pull_market_data()
		z = dict(list(x_1.items()))
	#print("The time for the page to get data {} ".format(time.time() - start_time))
	#with open('total_circulation.csv','w') as f:
	#	for key in z.keys():
	#		print(key,z[key])
	#		f.write("%s, %s\n" % (key,str(z[key])))

		with open('total_circulation.txt','w') as f:
			f.write(json.dumps(z))
		time.sleep(5)
#keep_refreshing_anchor()

def anchor_data():
	f = open('total_circulation.txt')
	y = json.load(f)
	print(y['Total_Value_locked'])
	print(y)
	print(type(y))
#anchor_data()
