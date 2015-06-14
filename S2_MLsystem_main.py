# -*- coding: utf-8 -*-
#!usr/bin/python
"""
Created on Sat Jun 13 09:49:34 2015

@author: nxh
"""

import datetime
import Database_Init as di
import S2_MLsystem_core as mls
import os

def mainProcess():
    # 0.configuration
    holdingHistoryTable = 's2_mls_holdingHistory'
    currentHoldingTable = 's2_mls_currentHolding'
    earningTable = 's2_mls_earningTable'
    num = 10    # max number of stocks in this portfolio
    startdate = "2015-01-01"
    amount = 10000  # amount of the new portfolio
    tradedate = datetime.datetime.strptime(startdate,'%Y-%m-%d').date()
    
    # 1.create database
    di.database_init(holdingHistoryTable,currentHoldingTable,earningTable,startdate,amount);
    
    # 2.decide the start date to complement the data
    #today = datetime.datetime.today().date()
    today = datetime.date(2015,2,20)    
    tradedate = mls.startdateGet(tradedate,earningTable)
    
    # 3. create the temporary variable directory
    if ~os.path.isdir('s2_mls'):
        os.mkdir(r's2_mls')
    
    # 4.run the strategy for each trading day
    while tradedate <= today:
        print tradedate
        subProcess(currentHoldingTable, holdingHistoryTable, earningTable, num, tradedate, amount)
        tradedate += datetime.timedelta(1)



def subProcess(currentHoldingTable, holdingHistoryTable, earningTable, num, tradedate, amount):
    # 4.1 check the currentHolding table to decide whether to make changes
    items = mls.checkCurrent(currentHoldingTable,num)    #item = (int, list)
    if items[0] == 0: # no changes in current portfolio
        newStocklist = []
    else:   # new portfolio
        newStocklist = mls.strategy_main(items[0])
    
    # 4.2 make change to the tables
    di.tableArrange(items, newStocklist, currentHoldingTable, holdingHistoryTable, num, tradedate)
    
    # 4.3 generate earning table
    di.earningTable(currentHoldingTable, earningTable, tradedate)
    
mainProcess()