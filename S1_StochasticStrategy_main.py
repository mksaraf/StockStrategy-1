# -*- coding: utf-8 -*-
#!usr/bin/python
"""
Created on Sat May 23 10:41:34 2015

@author: nxh
"""

import datetime
import Database_Init as di
import S1_StochasticStrategy_core as ss

def mainProcess():
    # 0.configuration
    holdingHistoryTable = 's1_test_holdingHistory'
    currentHoldingTable = 's1_test_currentHolding'
    earningTable = 's1_test_earningTable'
    num = 10    # max number of stocks in this portfolio
    startdate = "2015-01-01"
    amount = 10000  # amount of the new portfolio
    tradedate = datetime.datetime.strptime(startdate,'%Y-%m-%d').date()
    
    # 1.create database
    di.database_init(holdingHistoryTable,currentHoldingTable,earningTable,startdate,amount);
    
    # 2.decide the start date to complement the data
    #today = datetime.datetime.today().date()
    today = datetime.date(2015,1,20)    
    tradedate = ss.startdateGet(tradedate,earningTable)
    
    # 3.run the strategy for each trading day
    while tradedate <= today:
        subProcess(currentHoldingTable, holdingHistoryTable, earningTable, num, tradedate, amount)
        tradedate += datetime.timedelta(1)



def subProcess(currentHoldingTable, holdingHistoryTable, earningTable, num, tradedate, amount):
    # 3.1 check the currentHolding table to decide whether to make changes
    items = ss.checkCurrent(currentHoldingTable,num)    #item = (int, list)
    if items[0] == 0: # no changes in current portfolio
        newStocklist = []
    else:   # new portfolio
        newStocklist = ss.strategy_main(items[0])
    
    # 3.2 make change to the tables
    di.tableArrange(items, newStocklist, currentHoldingTable, holdingHistoryTable, num, tradedate)
    
    # 3.3 generate earning table
    
    
mainProcess()