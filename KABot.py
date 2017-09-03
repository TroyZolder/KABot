#!/usr/bin/env python
# This program buys some Dogecoins and sells them for a bigger price
from bittrex import Bittrex

# Get these from https://bittrex.com/Account/ManageApiKey
api = Bittrex('3e79067f35b14fa29a8feb56dcf88b9d', '5c53898f04624919b5bac546db5fec71')

# Market to trade at
trade = 'BTC'
currency = 'DOGE'
market = '{0}-{1}'.format(trade, currency)
# Amount of coins to buy
amount = 1300.0
# How big of a profit you want to make
multiplier = 1.1

# Getting the BTC price for DOGE
#dogesummary = api.get_markets('BTC-DOGE',market)
#dogeprice = dogesummary[0]['Last']
dogeprice = 0.00000040
print("The price for {0} is {1:.8f} {2}.".format(currency, dogeprice, trade))

# Buying 100 DOGE for BTC
print("Buying {0} {1} for {2:.8f} {3}.".format(amount, currency, dogeprice, trade))
print(api.buy_limit(market, amount, dogeprice)['success'])

# Multiplying the price by the multiplier
dogeprice = round(dogeprice*multiplier, 8)

# Selling 100 DOGE for the  new price
print("Selling {0} {1} for {2:.8f} {3}.".format(amount, currency, dogeprice, trade))
print(api.sell_limit(market, amount, dogeprice)['success'])

# Gets the DOGE balance
dogebalance = api.get_balance(currency)
print("Your balance is {0} {1}.".format(dogebalance['result']['Available'], currency))

# For a full list of functions, check out bittrex.py or https://bittrex.com/Home/Api
