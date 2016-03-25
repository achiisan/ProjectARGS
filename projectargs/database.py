#!/usr/bin/python

import sqlite3
import sqlitebck
from parser import  Parser

class Database:

		def __init__(self):
			self.r = sqlite3.connect(":memory:")
			print("Database Opened Successfully")

		def savetofile(self):
			filedb = sqlite3.connect("../database/projectargs.db");
			sqlitebck.copy(self.r, filedb)
		def loadfromfile(self):
			filedb = sqlite3.connect("../database/projectargs.db");
			sqlitebck.copy(filedb, self.r)
		def loadClasslist(self):
			filebuf = Parser.fileread("../schedule-list/classlist-2015-1.csv")
			classlist = filebuf.split("\n")
			
			self.r.execute("CREATE TABLE IF NOT EXISTS subjectlist (coursecode TEXT, section TEXT, class_size INTEGER, time TEXT, day TEXT, room TEXT, pri_instructor TEXT, sec_instructor TEXT)")
			self.r.commit()
			for cls in classlist:
			

				contents = cls.split(",")
		
		
				if len(contents) > 1:
					print(len(contents))
					self.r.execute("INSERT INTO subjectlist (coursecode, section, class_size, time, day, room, pri_instructor, sec_instructor) VALUES ('"+contents[0]+"','"+contents[1]+"','"+contents[2]+"','"+contents[3]+"','"+contents[4]+"','"+contents[5]+"','"+contents[6]+"','"+contents[7]+"')")
					self.r.commit()
			
			self.savetofile()
		def loadStudentList(self):
			filebuf = Parser.fileread("../fwdanonymizeddata/anon_PREDICTIONS")
			
			splitter = filebuf.split("###")
			
			students = splitter[1].split("#")
			count = 0;
			self.r.execute("CREATE TABLE IF NOT EXISTS studentlist (stdno TEXT, name TEXT, gender TEXT, country INTEGER, curriculum TEXT, scholarship TEXT, college TEXT, earned INTEGER, classif INTEGER, yearlevel INTEGER, allowed INTEGER,  grp TEXT, npriority INTEGER, nalternates INTEGER, ncurrent INTEGER)")
			self.r.commit()
			
			for student in students:
				#print(student)
				studinfo = student.split("\n")
				gotInfo = False
				for info in studinfo:
					if info.strip() != '' :
						ic = info.split(",")
						if gotInfo == False:
							self.r.execute("INSERT INTO studentlist VALUES('"+ic[0]+"','"+ic[1]+"','"+ic[2]+"',"+ic[3]+",'"+ic[4]+"','"+ic[5]+"','"+ic[6]+"',"+ic[7]+","+ic[8]+","+ic[9]+","+ic[10]+","+ic[11]+","+ic[12]+","+ic[13]+","+ic[14]+")")
							count = count + 1
							print(chr(27) + "[2J")
							print("Saving Student#: ",count)
							gotInfo = True
							self.r.execute("CREATE TABLE IF NOT EXISTS'"+ic[0]+"' (SCHOOL YEAR TEXT, TERM TEXT, COURSE TEXT,SECTION TEXT, UNITS TEXT, GRADE TEXT, COURSERANK TEXT, CONTRIB TEXT)")
						else:
							self.r.execute("INSERT INTO '"+ic[0]+ "' VALUES('"+ic[1]+"','"+ic[2]+"','"+ic[3]+"','"+ic[4]+"','"+ic[5]+"','"+ic[6]+"','"+ic[7]+"','"+ic[8]+"')")

			self.r.commit()

			self.savetofile()
			
