#!usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:27:35 2015

@author: nxh
"""

import MySQLdb
import random as rd

def checkCurrent(currentHoldingTable,num):
    conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="strategyDatabase")
    cursor = conn.cursor()
    sql = "select * from",currentHoldingTable,"order by buydate"
    cursor.execute(sql)
    
    if cursor.rowcount == 1:   # empty table
        cursor.close()
        return num
    else:
        print "Rows selected:", cursor.rowcount
        for row in cursor.fetchall():
            print "note:", row[0], row[1]
        cursor.close()
        return True            


def strategy_main(n):
    conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="StockDataInfoCenter")
    cursor = conn.cursor()
    sql = "select * from","StockInfoList"
    cursor.execute(sql)
    data = cursor.fetchall();
    stocklist = data[1]
    return strategy_core(stocklist,n)


def strategy_core(stocklist,n):
    loc = rd.sample(xrange(len(stocklist)),n)
    return [stocklist[i] for i in loc]
    
    
checkCurrent('s1_test_currentHolding')