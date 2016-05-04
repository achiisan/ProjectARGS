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



		
loadfromfile("projectargs.db")
#loadfromfile("curriculum.db")
print("Database Opened Successfully")	