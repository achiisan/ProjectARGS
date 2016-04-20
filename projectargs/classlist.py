#/usr/bin/python

import database
import re #regex
from parser import Parser

#Classlist function (LIST OF ALL CLASSES TO BE OFFERED IN A SEMESTER)
#Take note that THIS IS DIFFERENT FROM the SUBJECTS in the curriculum, as
#THe subjects in the curriculum may or may not be included in the subjects
#offered

classes = {}

#load classlist from file 

def loadClasslist():
	filebuf = Parser.fileread("../schedule-list/classlist-2015-1.csv")
	classlist = filebuf.split("\n")

	database.query("CREATE TABLE IF NOT EXISTS subjectlist (coursecode TEXT, section TEXT, class_size INTEGER, time TEXT, day TEXT, room TEXT, pri_instructor TEXT, sec_instructor TEXT, avail_slots INTEGER, lecture_comp TEXT)")
	database.commit()

	tempLecture = None

	for cls in classlist:


		contents = cls.split(",")


		if len(contents) > 1:

			print(contents[1])		
			if re.match("[A-Za-z0-9]*\-[0-9]*[LR]", contents[1] ):
				print("Recit")
				database.query("INSERT INTO subjectlist (coursecode, section, class_size, time, day, room, pri_instructor, sec_instructor, avail_slots, lecture_comp) VALUES ('"+contents[0]+"','"+contents[1]+"',"+contents[2]+",'"+contents[3]+"','"+contents[4]+"','"+contents[5]+"','"+contents[6]+"','"+contents[7]+"',"+contents[2]+",'"+tempLecture[1]+"')")


			else:
				print("Lecture")
				tempLecture = contents
				database.query("INSERT INTO subjectlist (coursecode, section, class_size, time, day, room, pri_instructor, sec_instructor, avail_slots, lecture_comp) VALUES ('"+contents[0]+"','"+contents[1]+"',"+contents[2]+",'"+contents[3]+"','"+contents[4]+"','"+contents[5]+"','"+contents[6]+"','"+contents[7]+"',"+contents[2]+",'None')")
	database.commit()

	database.savetofile()

def getClass(coursecode):
	buf = database.query("SELECT * FROM subjectlist WHERE COURSECODE = '"+coursecode+"'")

	return buf

def getClass(coursecode, section):
	buf = database.query("SELECT * FROM subjectlist WHERE COURSECODE = '"+coursecode+"'")

	return buf

def identifyLecture():
	print("X")







