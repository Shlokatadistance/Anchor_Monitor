import requests
import bs4 as bs
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import re


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
	dict_1 = {'Total Value locked':total_value_locked.text,
	'total Yield reserve':yield_reserve.text,
	'Total Collateral': total_collateral.text,
	'Total Deposit': total_deposit.text
	}

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

	dict_1 = {'ANC Price (UST)' : anc_price.text}
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

	dict_1 = {'ANC Buyback (72HR)(UST)': anc_buyback_hours,
	'ANC Buyback (12 Month) (UST)' : anc_buyback_total}

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

	dict_1 = {'Total Deposit': total_deposit,
	'Deposit APY' : deposit_apy,
	'Total Borrow' : total_borrow,
	'Borrow APR' : borrow_apr,
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

	dict_1 = {'Bonded Luna Price ': bluna_price,
	'Bonded Luna Collateral' : bluna_collateral,
	'Bonded Luna Total Collateral Value' : bluna_total_collateral_value,
	'Bonded Ether Price' : beth_price,
	'Bonded Ether Collateral' : beth_collateral,
	'Bonded Ether Total Collateral Value' : beth_total_collateral_value}

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
def anchor_data():
	path = '/Users/singularity/Hex/chromedriver'
	driver = webdriver.Chrome(path)
	url = 'https://app.anchorprotocol.com/'
	driver.get(url)
	time.sleep(4.5)
	page = driver.page_source
	#soup = BeautifulSoup(page,'html.parser')
	#print(soup)

	driver.quit()
	x_1 = total_circulation(page)
	x_2 = ANC_stats(page)
	x_3 = buyback_stats(page)
	x_4 = stablecoin_market(page)
	x_5 = bonded_prices(page)
	z = dict(list(x_1.items()) + list(x_2.items()) + list(x_3.items()) + list(x_4.items()) + list(x_5.items()))

	print(z)
main()



