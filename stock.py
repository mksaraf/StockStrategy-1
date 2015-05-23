#!usr/bin/python
# -*- coding: utf-8 -*-

#import numpy as np
import MySQLdb

def coreFunction():
    conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="historicalDatabase")
    cursor = conn.cursor()
    sql = "select * from t600000 order by tradedate"
    cursor.execute(sql)
    print "Rows selected:", cursor.rowcount
    for row in cursor.fetchall():
        print "note:", row[0], row[1]
    cursor.close()

#mat = 

if __name__=='__main__':
    coreFunction()