#!usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:27:35 2015

@author: nxh
"""

import MySQLdb
import random as rd
import datetime

def startdateGet(tradedate,earningTable):
    conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="strategyDatabase")
    cursor = conn.cursor()
    sql = "select * from " + earningTable + " order by tradedate desc limit 1"
    cursor.execute(sql)
    data = cursor.fetchall()
    if cursor.rowcount <= 0:
        pass
    else:
        sql = "select max(tradedate) from " + earningTable
        cursor.execute(sql)
        data = cursor.fetchall()
        tradedate = max(tradedate, data[0][0] + datetime.timedelta(1))
    
    cursor.close()
    conn.close()
    return tradedate
    

def checkCurrent(currentHoldingTable,num):
    conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="strategyDatabase")
    cursor = conn.cursor()
    sql = "select * from " + currentHoldingTable + " where stockid != '000000'"
    cursor.execute(sql)
    data = cursor.fetchall()
    
    if cursor.rowcount <= 1:   # empty table
        newStocklist = (num,[])
    else:
        stocklist = [datum[1] for datum in data]
        newStocklist = (num - len(data[1]) + len(data[1]), stocklist)
    
    cursor.close()
    conn.close()
    return newStocklist
    

def strategy_main(n):
    conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="StockDataInfoCenter")
    cursor = conn.cursor()
    sql = "select * from " + "StockInfoList"
    cursor.execute(sql)
    data = cursor.fetchall();
    stocklist = [datum[1] for datum in data]
    conn.close()
    return strategy_core(stocklist,n)


def strategy_core(stocklist,n):
    loc = rd.sample(xrange(len(stocklist)),n)
    return [stocklist[i] for i in loc]
    