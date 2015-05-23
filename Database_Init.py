#!usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 10:50:31 2015

@author: nxh
"""

import MySQLdb

def database_init(holdingHistory,currentHolding,earningTable,startdate,amount):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="strategyDatabase")
    cursor = conn.cursor()
    sql = "create table if not exists " + holdingHistory + ('('
    'id int unsigned auto_increment primary key, '
    'stockid char(6) not null, '
    'buydate date not null, '
    'selldate date not null, '
    'price float not null, '
    'amount float not null'
    ')')
    cursor.execute(sql)

    sql = "create table if not exists " + currentHolding + ('('
    'id int unsigned auto_increment primary key,'
    'stockid char(6) not null, '
    'buydate date not null, '
    'price float not null, '
    'amount float not null'
    ')')
    cursor.execute(sql)

    sql = "create table if not exists " + earningTable + ('('
    'id int unsigned auto_increment primary key,'
    'tradedate date not null, '
    'amount float not null'
    ')')
    cursor.execute(sql)
    
    # initialize the current holding table
    sql = "select * from " + currentHolding + " order by buydate"
    cursor.execute(sql)
    if cursor.rowcount <= 0:
        sql = 'insert into ' + currentHolding + '(stockid,buydate,price,amount) values("000000","' + startdate + '",1,' + str(amount) + ')'
        print sql        
        cursor.execute(sql)
    
    conn.commit()
    cursor.close()
    conn.close()