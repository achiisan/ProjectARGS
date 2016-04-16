#!/usr/bin/python


import database
from parser import Parser

#List of all students in the database. The load student list LOADS a PREDICTION 
#file from REGIST. This will be the basis for the prediction of ARGS

#Each student will be created a database table which will house the predictions 
#that will be used for alloting students


def loadStudentList():
	filebuf = Parser.fileread("../fwdanonymizeddata/anon_PREDICTIONS")

	splitter = filebuf.split("###")

	students = splitter[1].split("#")
	count = 0;
	database.query("CREATE TABLE IF NOT EXISTS studentlist (stdno TEXT, name TEXT, gender TEXT, country INTEGER, curriculum TEXT, scholarship TEXT, college TEXT, earned INTEGER, classif INTEGER, yearlevel INTEGER, allowed INTEGER,  grp TEXT, npriority INTEGER, nalternates INTEGER, ncurrent INTEGER)")
	database.commit()

	for student in students:
		#print(student)
		studinfo = student.split("\n")
		gotInfo = False
		for info in studinfo:
			if info.strip() != '' :
				ic = info.split(",")
				if gotInfo == False:
					database.query("INSERT INTO studentlist VALUES('"+ic[0]+"','"+ic[1]+"','"+ic[2]+"',"+ic[3]+",'"+ic[4]+"','"+ic[5]+"','"+ic[6]+"',"+ic[7]+","+ic[8]+","+ic[9]+","+ic[10]+","+ic[11]+","+ic[12]+","+ic[13]+","+ic[14]+")")
					count = count + 1
					print(chr(27) + "[2J")
					print("Saving Student#: ",count)
					gotInfo = True
					database.query("CREATE TABLE IF NOT EXISTS'"+ic[0]+"' (SCHOOL YEAR TEXT, TERM TEXT, COURSE TEXT,SECTION TEXT, UNITS TEXT, GRADE TEXT, COURSERANK TEXT, CONTRIB TEXT)")
				else:
					database.query("INSERT INTO '"+ic[0]+ "' VALUES('"+ic[1]+"','"+ic[2]+"','"+ic[3]+"','"+ic[4]+"','"+ic[5]+"','"+ic[6]+"','"+ic[7]+"','"+ic[8]+"')")

	database.commit()

	database.savetofile()
