import requests
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
x = pull_market_data()
print(x)