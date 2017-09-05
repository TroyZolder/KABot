#!/usr/bin/env python
# This program buys some Dogecoins and sells them for a bigger price
from bittrex import Bittrex
import re
import json
import matplotlib.pyplot as plt
import numpy as np

# Get APIkeys from https://bittrex.com/Account/ManageApiKey
# and put them in a APIkeys.txt file in the same folder with
# the following format:
# Key = yourKeyHere
# Secret = yourSecretKeyHere

with open("APIkeys.txt") as r:
    for line in r:
        if line.startswith('Key = '):
            number = line.partition('= ')[2]
            number = re.sub('\n', '',number)
        if line.startswith('Secret = '):
            number2 = line.partition('= ')[2]

api = Bittrex(number, number2)

# Market to trade at
trade = 'BTC'
#currency, e.g. 'DOGE', 'XRP' etc.
#currency = input("Currency? (BTC-xxx), e.g. DOGE or XRP:")

currencyList = ['DOGE','XRP','LTC','XMR','DOPE','ETH']
currencyListLength = len(currencyList)
movingAvgs = [None]*currencyListLength
linearFit = [None]*currencyListLength
m = [None]*currencyListLength
b = [None]*currencyListLength

for c in range (0,currencyListLength):
    currency = currencyList[c]

    market = '{0}-{1}'.format(trade, currency)

    # Download and store JSON file containing all ticks
    jsonFile = api.get_ticks(market)['result']
    # Count number of ticks (or the objects in JSON file):
    lengthTicker = len(api.get_ticks(market)['result'])

    print(market)
    print("oldest \"last\" value, index 0:")
    print(jsonFile[0]['L'])

    print("newest \"last\" value, index {0}:".format(lengthTicker))
    print(jsonFile[lengthTicker-1]['L'])

    # Moving average:
    sumTicks = 0
    avgTicks = 0

    # period to average over:
    avgPeriod = 10
    # how much time to go back e.g. 50 with oneMin intervals = 50 min:
    backTimeIntervals = 120
    movingAvg = [None]*backTimeIntervals
    arrayX = np.linspace(1., backTimeIntervals, backTimeIntervals)

    for y in range (1,backTimeIntervals+1):
        for x in range (y, y+avgPeriod):
            sumTicks = sumTicks + jsonFile[lengthTicker-x]['L']
        avgTicks = sumTicks/avgPeriod
        #print(avgTicks)
        movingAvg[y-1] = avgTicks
        sumTicks = 0

    movingAvgs[c] = movingAvg

    # for linear regression/fit (http://stattrek.com/regression/regression-example.aspx?Tutorial=AP)
    m[c],b[c] = np.polyfit(arrayX, movingAvg, 1)
    
    '''
    movingAvgMeanY = sum([x/backTimeIntervals for x in movingAvg])
    movingAvgMinusMeanY = movingAvg
    movingAvgMinusMeanY = [x - movingAvgMeanY for x in movingAvgMinusMeanY]
    movingAvgMinusMeanYSquared = [x*x for x in movingAvgMinusMeanY]

    arrayXMean = sum([x/backTimeIntervals for x in arrayX])
    arrayXMinusMean = arrayX
    arrayXMinusMean = [x - arrayXMean for x in arrayXMinusMean]
    #arrayXMinusMeanSquared = [x*x for x in arrayXMinusMean]

    b1 = sum(arrayXMean - movingAvgMinusMeanY)/sum(movingAvgMinusMeanYSquared)
    b0 = arrayXMean - b1*movingAvgMeanY
    linearFit[c] = b0 + b1*arrayX
    '''
for k in range(0,currencyListLength):    
    plt.subplot(3,2,k+1)
    plt.plot(arrayX,movingAvgs[k])
    plt.plot(arrayX,m[k]*arrayX+b[k])

    plt.title('{0}-{1}'.format(trade, currencyList[k]))
    plt.ylabel('value [BTC]')
    plt.xlabel('t [min]')
    plt.gca().invert_xaxis()
    plt.grid(True)

plt.tight_layout()
plt.show()

'''
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
'''
# For a full list of functions, check out bittrex.py or https://bittrex.com/Home/Api

input("Press Enter to continue...")
