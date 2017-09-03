#!/usr/bin/env python
# This program buys some Dogecoins and sells them for a bigger price
from bittrex import Bittrex

# Get these from https://bittrex.com/Account/ManageApiKey
api = Bittrex('3e79067f35b14fa29a8feb56dcf88b9d', '5c53898f04624919b5bac546db5fec71')

# Market to trade at
trade = 'BTC'
#currency = 'DOGE'
currency = input("Currency? (BTC-xxx), e.g. DOGE:")

market = '{0}-{1}'.format(trade, currency)

# How big of a profit you want to make
multiplier = 1.1

# Gets the balance for the chosen currency
currentBalance = api.get_balance(currency)
print("Your balance is {0} {1}.".format(currentBalance['result']['Available'], currency))

# Getting the BTC price for DOGE
priceInBTC = api.get_ticker(market)['result']['Last']
priceInSat = api.get_ticker(market)['result']['Last']*1e8

print("The price for {0} is {1:.8f} {2} or {3:.0f} Satoshi.".format(currency, priceInBTC, trade, priceInSat))

# Amount of coins to buy
amount = input("Amount to buy:")

# Buying 100 DOGE for BTC
print("Buying {0} {1} for {2:.8f} {3}.".format(amount, currency, priceInBTC, trade))
print(api.buy_limit(market, amount, priceInBTC)['success'])

# Multiplying the price by the multiplier
dogeprice = round(priceInBTC*multiplier, 8)

# Selling:
print("Selling {0} {1} for {2:.8f} {3}.".format(amount, currency, priceInBTC, trade))
print(api.sell_limit(market, amount, priceInBTC)['success'])

# For a full list of functions, check out bittrex.py or https://bittrex.com/Home/Api

input("Press Enter to continue...")
