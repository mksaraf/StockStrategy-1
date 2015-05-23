# -*- coding: utf-8 -*-
#!usr/bin/python
"""
Created on Sat May 23 10:41:34 2015

@author: nxh
"""

import Database_Init as di
#import S1_StochasticStrategy_core as ss

holdingHistoryTable = 's1_test_holdingHistory'
currentHoldingTable = 's1_test_currentHolding'
earningTable = 's1_test_earningTable'
num = 10    # max number of stocks in this portfolio
startdate = "2015-01-01"
amount = 10000  # amount of the new portfolio


# 1.create database
di.database_init(holdingHistoryTable,currentHoldingTable,earningTable,startdate,amount);


# 2.apply the strategy and get the operate actions
# 2.1 check the currentHolding table to decide whether make changes
#items = ss.checkCurrent(currentHoldingTable,num)    #item = (new numbers, [sell id_1, sell id_2, ...])
#if len(items) == 0: # no changes in current portfolio
#    pass
#elif items == num:   # new portfolio
#    ss.strategy_main(items)
#else:
#    pass


# 3. generate earning table
