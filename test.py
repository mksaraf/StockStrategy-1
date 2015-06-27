# -*- coding: utf-8 -*-
"""
Created on Sun May 31 08:52:19 2015

@author: nxh
"""

import MySQLdb
import matplotlib.pyplot as plt
import os
import numpy as np

def movavg(values,window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma
    
def movsum(values,window):
    weights = np.repeat(1.0, window)
    sma = np.convolve(values, weights, 'valid')
    return sma

def movcost(amount,vol,weight,window):
    sma = movsum(amount,window)/movsum(vol/weight,window)
    return sma

def movprofit(cost,vol,weight,amount,window):
    cumvol = movsum(vol/weight,window)
    cumamount = movsum(amount,window)
    profit = cost[window:]*cumvol[:-1] - cumamount[:-1]
    return profit
    
    

if not os.path.isdir('s2_mls'):
    os.mkdir(r's2_mls')
    
conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="StockDataInfoCenter")
cursor = conn.cursor()
sql = "select * from " + "StockInfoList"
cursor.execute(sql)
data = cursor.fetchall()
stocklist = [datum[1] for datum in data]

conn_h = MySQLdb.connect(host="localhost",user="root",passwd="root",db="historicalDatabase")
cursor_h = conn_h.cursor()
conn_c = MySQLdb.connect(host="localhost",user="root",passwd="root",db="updateDatabase")
cursor_c = conn_c.cursor()

for stock in stocklist[0:1]:
    sql = "select * from t" + stock + " order by tradedate asc"
    cursor_h.execute(sql)
    data = cursor_h.fetchall()
    price = np.array([datum[4] for datum in data])
    vol = np.array([datum[6] for datum in data])
    amount = np.array([datum[7] for datum in data])
    weight = np.array([datum[8] for datum in data])
    
    cursor_c.execute(sql)
    data = cursor_c.fetchall()
    price = np.hstack((price, np.array([datum[4] for datum in data])))
    vol = np.hstack((vol, np.array([datum[6] for datum in data])))
    amount = np.hstack((amount, np.array([datum[7] for datum in data])))
    weight = np.hstack((weight, np.array([datum[8] for datum in data])))
    
    cost = amount/vol*weight
    x = range(0,len(cost))
    
    
    #==========================
    # start plot
    #==========================
    f, axarr = plt.subplots(2, sharex=True)
    
    # moving average of cost price
    
    
    axarr[0].plot(x,cost,'.-')
    axarr[0].plot(x[4:],movcost(amount,vol,weight,5))
    axarr[0].plot(x[9:],movcost(amount,vol,weight,10))
    axarr[0].plot(x[19:],movcost(amount,vol,weight,20))
    axarr[0].plot(x[29:],movcost(amount,vol,weight,30))
    axarr[0].plot(x[59:],movcost(amount,vol,weight,60))
    
    '''
    # accumulate trading cash
    a1 = movsum(amount,5)
    a2 = movsum(amount,10)
    a3 = movsum(amount,20)
    a4 = movsum(amount,30)
    a5 = movsum(amount,60)
    #axarr[1].plot(x,a1/max(a1)*max(price))
    axarr[1].plot(x[4:],a1/max(a5)*max(price))
    axarr[1].plot(x[9:],a2/max(a5)*max(price))
    axarr[1].plot(x[19:],a3/max(a5)*max(price))
    axarr[1].plot(x[29:],a4/max(a5)*max(price))
    axarr[1].plot(x[59:],a5/max(a5)*max(price))
    '''
    '''
    # moving average of tradding cash
    #plt.plot(x,amount,'.-')
    axarr[1].plot(x[4:],movavg(amount,5))
    axarr[1].plot(x[9:],movavg(amount,10))
    axarr[1].plot(x[19:],movavg(amount,20))
    axarr[1].plot(x[29:],movavg(amount,30))
    axarr[1].plot(x[59:],movavg(amount,60))
    '''
    '''
    # moving sum of trading shares (fixed)
    v1 = movsum(vol/weight,5)
    v2 = movsum(vol/weight,10)
    v3 = movsum(vol/weight,20)
    v4 = movsum(vol/weight,30)
    v5 = movsum(vol/weight,60)
    #axarr[1].plot(x,a1/max(a1)*max(price))
    axarr[1].plot(x[4:],v1/max(v5)*max(price))
    axarr[1].plot(x[9:],v2/max(v5)*max(price))
    axarr[1].plot(x[19:],v3/max(v5)*max(price))
    axarr[1].plot(x[29:],v4/max(v5)*max(price))
    axarr[1].plot(x[59:],v5/max(v5)*max(price))
    '''
    
    # accumulate field curve
    pro1 = movprofit(cost,vol,weight,amount,5)
    pro2 = movprofit(cost,vol,weight,amount,10)
    pro3 = movprofit(cost,vol,weight,amount,20)
    pro4 = movprofit(cost,vol,weight,amount,30)
    pro5 = movprofit(cost,vol,weight,amount,60)
    axarr[1].plot(x[5:],pro1)
    axarr[1].plot(x[10:],pro2)
    axarr[1].plot(x[20:],pro3)
    axarr[1].plot(x[30:],pro4)
    axarr[1].plot(x[60:],pro5)
    
    slen = len(pro4)
    t1 = np.sign(pro2[-slen:] - pro1[-slen:])
    t2 = np.sign(pro3[-slen:] - pro2[-slen:])
    t3 = np.sign(pro4 - pro3[-slen:])
    
    t = t1+t2+t3
    tt = t[:-2]-t[2:]
    xx = [i for i,a in enumerate(tt) if a == 6]
    axarr[1].plot(xx,np.repeat(0,len(xx)),'o')
    
    '''
    cumvol = vol/weight
    cumvol = np.cumsum(vol)
    yie = cumvol[:-1]*cost[1:]-np.cumsum(amount[:-1])
    axarr[1].plot(x[1:],yie)
    '''
    
    plt.show()
    

    
# close database
cursor_h.close()
conn_h.close()
cursor_c.close()
conn_c.close()


