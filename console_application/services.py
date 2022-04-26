import requests
import bs4 as bs
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import re
import time
from apscheduler.schedulers.background import BackgroundScheduler as scheduler
import mpld3
from mpld3 import plugins

def get_graphs():
	r_1 = requests.get("https://api.anchorprotocol.com/api/v1/deposit/1d")
	r_2  = requests.get("https://api.anchorprotocol.com/api/v1/borrow/1d")

	x = r_1.json()
	list_0 = []
	list_0_1 = []
	print(x)
	for i in x['total_ust_deposits']:
		#print(i)
		list_0.append(float(i['deposit']))
		list_0_1.append(float(i['timestamp']))
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
	ax.plot(list_2,list_1,'r',label='Borrow')
	ax.plot(list_0_1,list_0,'g',label='Deposit')
	xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
	ax.set_xlabel('TimeStamps')
	ax.set_ylabel('Prices(in million UST)')
	#ax.xaxis.set_major_formatter(xfmt)
	ax.legend()
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
	g = mpld3.fig_to_html(fig)
	mpld3.show()
	mpld3.save_html(fig,'graph.html')
	#return HttpResponse(g)

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

def ANC_stats(page):
	soup = BeautifulSoup(page,'html.parser')
	predicate = {'class':re.compile('.*anc-price.*')}
	content = soup.find_all(**predicate)
	#print(type(content))
	#print(content[0])
	x = content[0]
	#y = x.find('section')
	#print(y)
	content_0 = x.find('div',attrs={'class':'NeuSection-content'})
	anc_price = content_0.find('p',attrs={'class':'amount'})
	#print(anc_price.text)

	dict_1 = {'ANC_Price_UST' : anc_price.text}
	return dict_1


def buyback_stats(page):
	soup = BeautifulSoup(page,'html.parser')
	predicate = {'class':re.compile('.*anc-buyback.*')}
	content = soup.find_all(**predicate)
	x = content[0]
	#print(x)
	#content = soup.find('section',attrs={'class':'NeuSection-root sc-dvQaRk jMuSqd anc-buyback'})
	content_1 = x.find('div',attrs={'class':'NeuSection-content'})
	content_2 = content_1.find_all('section')
	content_3 = content_2[0].find_all('div')
	#print(content_3)
	content_4 = content_3[0].find_all('p')
	anc_buyback_hours = content_4[1].text
	content_3_1 = content_2[1].find_all('div')
	content_4_1 = content_3_1[0].find_all('p')
	anc_buyback_total = content_4_1[1].text
	#print('ANC 72',anc_buyback_hours)
	#print('ANC total',anc_buyback_total)

	dict_1 = {'ANC_Buyback_72HR_UST': anc_buyback_hours,
	'ANC_Buyback_12Month_UST' : anc_buyback_total}

	return dict_1

	#both values in ust


def stablecoin_market(page):
	soup = BeautifulSoup(page,'html.parser')
	predicate = {'class':re.compile( '.*stablecoin*.')}
	content = soup.find(**predicate)
	#print(content)
	c_1 = content.find('div',attrs={'class':'NeuSection-content'})
	c_2 = c_1.find_all('div')
	c_3 = c_2[1].find('p',attrs={'class':'amount'})
	total_borrow = c_3.text
	
	#now the stablecoin_market
	predicate_2 = {'class':re.compile('.*stablecoin-market*.')}
	c_4 = c_1.find(**predicate_2)
	#print(c_4)
	c_5 = c_4.find_all('div',attrs={'class':'value'})
	total_deposit = c_5[0].text
	deposit_apy = c_5[1].text
	total_borrow = c_5[2].text
	borrow_apr = c_5[3].text
	#print("Total Deposit is {}".format(total_deposit))

	dict_1 = {'Total_Deposit': total_deposit,
	'Deposit_APY' : deposit_apy,
	'Total_Borrow' : total_borrow,
	'Borrow_APR' : borrow_apr,
	}
	return dict_1

def bonded_prices(page):
	soup = BeautifulSoup(page,'html.parser')
	predicate = {'class':re.compile('.*collaterals*.')}
	c = soup.find(**predicate)
	c_1 = c.find('div',attrs={'class':'NeuSection-content'})
	c_2 = c_1.find_all('div',attrs={'class':'value'})
	bluna_price = c_2[0].text
	bluna_collateral = c_2[1].text
	bluna_total_collateral_value = c_2[2].text
	beth_price = c_2[3].text
	beth_collateral = c_2[4].text
	beth_total_collateral_value = c_2[5].text
	#print("The value of bluna and beth is {} {}".format(bluna_price, beth_price))

	dict_1 = {'Bonded_Luna_Price': bluna_price,
	'Bonded_Luna_Collateral' : bluna_collateral,
	'Bonded_Luna_Total_Collateral_Value' : bluna_total_collateral_value,
	'Bonded_Ether_Price' : beth_price,
	'Bonded_Ether_Collateral' : beth_collateral,
	'Bonded_Ether_Total_Collateral_Value' : beth_total_collateral_value}

	return dict_1


def new_search(page):
	soup = BeautifulSoup(page,'html.parser')
	predicates = [
    {'id' : re.compile('.*anc.*')}, 
    {'class' : re.compile('.*anc.*')},
    ]
	for p in predicates:
		x = soup.find_all(**p)
		print(x)
def pull_market_data():
	tokens = ['USDTDAI','LUNAUSDT','ETHUSDT','BETHETH']
	#for bonded luna, use coingecko. 
	a = []
	dict_1 = {}
	for token in tokens:
		resp_binance = requests.get('https://api.binance.com/api/v3/ticker/price?symbol='+token)
		if resp_binance.status_code != 200:
			print(dict_1)
			resp_kraken = requests.get('https://api.kraken.com/0/public/Ticker?pair='+token)
			data_1 = resp_kraken.json()
			print("Token used {}".format(token))
			a.append(data_1)

		else:
			data_1 = resp_binance.json()
			a.append(data_1)
			#print(dict_1)
	for i in a:
		dict_1[i['symbol']] = i['price']
	return dict_1
def get_graphs():
	r_1 = requests.get("https://api.anchorprotocol.com/api/v1/deposit/1d")
	r_2  = requests.get("https://api.anchorprotocol.com/api/v1/borrow/1d")

	x = r_1.json()
	list_0 = []
	list_0_1 = []
	print(x)
	for i in x['total_ust_deposits']:
		#print(i)
		list_0.append(float(i['deposit']))
		list_0_1.append(float(i['timestamp']))
	list_1 = []
	list_2 = []
	y = r_2.json()
	for i in y:
		#print(i)
		list_1.append(float(i['total_borrowed']))
		list_2.append(float(i['timestamp']))
	plt.plot(list_2, list_1,'r')
	plt.plot(list_0_1,list_0,'g')
	plt.show()


def keep_refreshing_anchor():
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
	with open('total_circulation.csv','w') as f:
		for key in dict_1.keys():
			f.write("%s, %s\n" % (key,dict_1[key]))

		
def anchor_data():
	"""
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
	print("The time for the page to get data {} ".format(time.time() - start_time))
	"""
	f = open('total_circulation.txt')
	y = json.load(f)
	return y
def page_2():
	"""
	start_time = time.time()
	path = '/Users/singularity/Hex/chromedriver'
	op = webdriver.ChromeOptions()
	op.add_argument('headless')
	driver = webdriver.Chrome(path,options=op)
	url = 'https://app.anchorprotocol.com/'
	driver.get(url)
	time.sleep(3.5)
	page = driver.page_source
	driver.quit()
	
	x_2 = ANC_stats(page)
	x_3 = buyback_stats(page)
	x_4 = stablecoin_market(page)
	x_5 = bonded_prices(page)
	x_6 = pull_market_data()
	"""
	f = open('stats.txt')
	y = json.load(f)
	
	return y






"""

sch = scheduler()
sch.add_job(anchor_data, 'interval', seconds=5)
sch.start()
try:
	print("Scheduler has started")
	while 1:
		print("Now trying to get values")

		time.sleep(1)
except KeyboardInterrupt:
	if sch.state():
		sch.shutdown()

"""

