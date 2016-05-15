#!/usr/bin/python

#==========================================================
#DATABASE FUNCTION
# INSERT, DELETE, CREATE TABLE TO DATABASE


import sqlite3
import sqlitebck
from parser import  Parser


r = sqlite3.connect(":memory:")

#save to a custom DB
def savetofile( filename="projectargs.db"):
	filedb = sqlite3.connect("../database/"+filename);
	sqlitebck.copy(r, filedb)
def loadfromfile(filename="projectargs.db"):
	filedb = sqlite3.connect("../database/"+filename);
	sqlitebck.copy(filedb, r)

def query(query):
	#ADD SAFEGUARD CHECKER HERE SOON..

	ret = r.execute(query)
	return ret

def commit():
	r.commit()



#INTERCHANGE FOR ANALYTICS (REGIST FILES)
loadfromfile("projectargs.db")
#loadfromfile("regist.db")
#loadfromfile("projectargs_analysis2.db")
print("Database Opened Successfully")
