#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import csv

def deleteContent(fName):
    with open(fName, "w"):
        pass

deleteContent('train.csv')

with open('train.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    db = MySQLdb.connect(host="localhost",
                     user="askar",
                     passwd="",
                     db="KRISHA_DATA")
    cur = db.cursor()
    cur.execute("show columns from Houses")
    arr = []
    for col in cur.fetchall():
    	arr += [col[0]]
    print ', '.join(arr)
    spamwriter.writerow(arr)
    cur.execute("select * from Houses")
    for row in cur.fetchall():
   		arr = []
   		for col in row:
   			arr += [str(col)]
   		print ', '.join(arr)
   		spamwriter.writerow(arr)

    db.close()
