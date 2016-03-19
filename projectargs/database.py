#!/usr/bin/python

import sqlite3
from parser import  Parser

class Database:

		def __init__(self):
			self.r = sqlite3.connect("../database/projectargs.db")
			print("Database Opened Successfully")


		def loadClasslist(self):
			filebuf = Parser.fileread("../schedule-list/classlist-2015-1.csv")
			classlist = filebuf.split("\n")
			

			for cls in classlist:
			

				contents = cls.split(",")
		
		
				if len(contents) > 0:
					print(contents[1])
					self.r.execute("INSERT INTO subjectlist (coursecode, section, class_size, time, day, room, pri_instructor, sec_instructor) VALUES ('"+contents[0]+"','"+contents[1]+"','"+contents[2]+"','"+contents[3]+"','"+contents[4]+"','"+contents[5]+"','"+contents[6]+"','"+contents[7]+"')")
					self.r.commit()
					