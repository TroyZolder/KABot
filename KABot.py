#!/usr/bin/env python
# This program buys some Dogecoins and sells them for a bigger price
from bittrex import Bittrex

# Get these from https://bittrex.com/Account/ManageApiKey
api = Bittrex('3e79067f35b14fa29a8feb56dcf88b9d', '5c53898f04624919b5bac546db5fec71')

# Market to trade at
trade = 'BTC'
#currency, e.g. 'DOGE', 'XRP' etc.
currency = input("Currency? (BTC-xxx), e.g. DOGE or XRP:")
market = '{0}-{1}'.format(trade, currency)

# Gets the balance for the chosen currency
currentBalance = api.get_balance(currency)
print("You currently have {0} {1}.".format(currentBalance['result']['Available'], currency))

# Getting the BTC price for DOGE
priceInBTC = api.get_ticker(market)['result']['Last']
priceInSat = api.get_ticker(market)['result']['Last']*1e8

print("The price for {0} is {1:.8f} {2} or {3:.0f} Satoshi.".format(currency, priceInBTC, trade, priceInSat))

# Amount of coins to buy
buyPrice = input("Price to buy per coin (in Sat!):")
buyPriceInBTC = float(buyPrice)*float(1e-8)
buyAmount = input("Amount to buy: ")
buyCost = float(buyAmount)*float(buyPriceInBTC)

# Buying confirmation
print("Buying {0} {1} at {2} Sat, costing {4:.8f} {3}".format(buyAmount, currency, buyPrice, trade, buyCost))
buyConfirm = input("Confirm buy (y/n):")

if buyConfirm == 'y':
    print(api.buy_limit(market, buyAmount, buyPriceInBTC)['success'])
else:
    print("Buy cancelled")

# Amount of coins to sell
sellPrice = input("Price to sell per coin (in Sat!):")
sellPriceInBTC = float(sellPrice)*float(1e-8)
sellAmount = input("Amount to sell: ")
sellCost = float(sellAmount)*float(sellPriceInBTC)

# Multiplying the price by the multiplier
#dogeprice = round(priceInBTC*multiplier, 8)

# Selling confirmation
print("Selling {0} {1} for {2} Sat, yielding {4} {3}.".format(sellAmount, currency, sellPrice, trade, sellCost))
sellConfirm = input("Confirm sell (y/n):")

if sellConfirm == 'y':
    print(api.sell_limit(market, sellAmount, sellPriceInBTC)['success'])
else:
    print("Sell cancelled")

# For a full list of functions, check out bittrex.py or https://bittrex.com/Home/Api

input("Press Enter to continue...")
