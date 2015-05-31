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
    'buyprice float not null, '
    'sellprice float not null, '
    'amount float not null'
    ')')
    cursor.execute(sql)

    sql = "create table if not exists " + currentHolding + ('('
    'id int unsigned auto_increment primary key,'
    'stockid char(6) not null, '
    'buydate date not null, '
    'buyprice float not null, '
    'currentprice float not null, '
    'amount float not null'
    ')')
    cursor.execute(sql)

    sql = "create table if not exists " + earningTable + ('('
    'id int unsigned auto_increment primary key, '
    'tradedate date not null, '
    'amount float not null, '
    'quantity int not null'
    ')')
    cursor.execute(sql)
    
    # initialize the current holding table
    sql = "select * from " + currentHolding + " order by buydate"
    cursor.execute(sql)
    if cursor.rowcount <= 0:
        sql = 'insert into ' + currentHolding + '(stockid,buydate,buyprice,currentprice,amount) values("000000","' + startdate + '",1,1,' + str(amount) + ')'
        cursor.execute(sql)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    
def tableArrange(items, newStocklist, currentHolding, holdingHistory, num, tradedate):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="strategyDatabase")
    cursor = conn.cursor()
    conn_ud = MySQLdb.connect(host="localhost",user="root",passwd="root",db="updateDatabase")
    cursor_ud = conn_ud.cursor()
        
    # 1.move sell data into history table
    if items[1] == []:
        pass
    else:
        # 1.1 copy data
        sets = str(tuple(items[1]))
        if sets[-2] == ',':
            sets = sets[:-2]+sets[-1]
        sql = "select stockid,buydate,buyprice,amount from " + currentHolding + " where stockid in " + sets
        cursor.execute(sql)
        data = cursor.fetchall()
        data = list(data)
        data = [list(datum) for datum in data]
        
        # 1.1.1 check if open this trading date, if yes, find the open price as sell price
        newdata = []
        for datum in data:
            sql = "select open from t" + datum[0] + " where tradedate='" + str(tradedate) + "'"
            cursor_ud.execute(sql)
            sellprice = cursor_ud.fetchall()
            if sellprice == ():
                continue
            datum[1] = str(datum[1])
            datum.insert(2,str(tradedate))
            datum.insert(4,sellprice[0][0])
            newdata.append(datum)
            
        data = newdata
        # renew the sets
        sets = str(tuple([datum[0] for datum in data]))
        if sets[-2] == ',':
            sets = sets[:-2]+sets[-1]

        
        # 1.1.2 if no valid data, no following move actions
        if data == []:
            pass
        else:
            data = [tuple(datum) for datum in data]
            sql = "insert into " + holdingHistory + "(stockid,buydate,selldate,buyprice,sellprice,amount) values(%s,%s,%s,%s,%s,%s)"
            cursor.executemany(sql,data)
            conn.commit()
            
            # 1.2 delete the moved data
            # 1.2.1 get the market value of the sell stocks
            amount_add = sum([datum[4]/datum[3]*datum[5] for datum in data])
            
            # 1.2.2 add the market value to the cash account
            sql = "update " + currentHolding + " set amount=amount+" + str(amount_add) + " where stockid='000000'"
            cursor.execute(sql)        
            conn.commit()
            
            # 1.2.3 delete the sell stocks
            sql = "delete from " + currentHolding + " where stockid in " + sets
            cursor.execute(sql)
            conn.commit()
        
    
    # 2.add new data into current holding table
    # 2.1 adjust the new stock list, problem may caused by 1.1.1 (can't sell stock)
    sql = "select stockid,amount from " + currentHolding
    cursor.execute(sql)
    stocks = cursor.fetchall()
    rnum = cursor.rowcount - 1 + len(newStocklist) - num
    if rnum > 0:
        del newStocklist[-rnum:]
    
    # 2.2 start to insert
    if items[0] == 0 or newStocklist == []:
        pass
    else:
        # 2.2.1 get the cash account
        amount_rest = stocks[0][1]
        
        # 2.2.2 decide the invest amount for each new stock
        amount_each = amount_rest/items[0]
        
        # 2.2.3 insert data
        #conn.select_db('updateDatabase')
        reduceamount = 0
        for stock in newStocklist:
            sql = "select close from t" + stock + " where tradedate='" + str(tradedate) + "'"
            cursor_ud.execute(sql)
            data = cursor_ud.fetchall()
            if data == ():
                continue
            sql = "insert into " + currentHolding + "(stockid, buydate, buyprice, currentprice, amount) values(%s,%s,%s,%s,%s)"
            cursor.execute(sql, (stock,str(tradedate),data[0][0],data[0][0],amount_each))
            reduceamount += amount_each
        sql = "update " + currentHolding + " set amount=amount-" + str(reduceamount) + " where stockid='000000'"
        cursor.execute(sql)
        conn.commit()
    
    
    # 3. update the current price of each holding stock
    sql = "select stockid,amount from " + currentHolding
    cursor.execute(sql)
    stocks = cursor.fetchall()
    
    for stock in stocks[1:]:
        sql = "select close from t" + stock[0] + " where tradedate='" + str(tradedate) + "'"
        cursor_ud.execute(sql)
        data = cursor_ud.fetchall()
        if data == ():
            continue
        else:
            sql = "update " + currentHolding + " set currentprice=" + str(data[0][0]) + " where stockid=" + stock[0]
            cursor.execute(sql)
            conn.commit()
    
    conn.commit()
    cursor.close()
    conn.close()
    cursor_ud.close()
    conn_ud.close()
    
    
def earningTable(currentHolding, earningTable, tradedate):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="strategyDatabase")
    cursor = conn.cursor()
    
    sql = "select buyprice,currentprice,amount from " + currentHolding
    cursor.execute(sql)
    stocks = cursor.fetchall()
    cmv = stocks[0][2]
    for stock in stocks[1:]:
        cmv += stock[1]*stock[2]/stock[0]
    
    sql = "insert into " + earningTable + "(tradedate, amount, quantity) values('" + str(tradedate) + "'," + str(cmv) + "," + str(cursor.rowcount-1) + ")"
    cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()