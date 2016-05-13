#/usr/bin/python

import database
import re #regex
import subjecttree
from parser import Parser
import mongo_database
import os
from os import listdir
import re

#Classlist function (LIST OF ALL CLASSES TO BE OFFERED IN A SEMESTER)
#Take note that THIS IS DIFFERENT FROM the SUBJECTS in the curriculum, as
#THe subjects in the curriculum may or may not be included in the subjects
#offered

classes = {}

#load classlist from file

def loadClasslist():
	print("=================Loading Classlist..==================\n")
	filebuf = Parser.fileread("../schedule-list/classlist-2015-1.csv")
	classlist = filebuf.split("\n")

	database.query("CREATE TABLE IF NOT EXISTS subjectlist (coursecode TEXT, section TEXT, class_size INTEGER, time TEXT, day TEXT, room TEXT, pri_instructor TEXT, sec_instructor TEXT, avail_slots INTEGER, lecture_comp TEXT)")
	database.query("CREATE TABLE IF NOT EXISTS subjectlist_lecture (coursecode TEXT, section TEXT, class_size INTEGER, time TEXT, day TEXT, room TEXT, pri_instructor TEXT, sec_instructor TEXT, avail_slots INTEGER)")
	database.commit()

	tempLecture = None
	lectureDeleted = False

	for cls in classlist:


		contents = cls.split(",")


		if len(contents) > 1:


			if re.match("[A-Za-z0-9]*\-[0-9]*[LR]", contents[1] ):
				#print("Recit")
				database.query("INSERT INTO subjectlist (coursecode, section, class_size, time, day, room, pri_instructor, sec_instructor, avail_slots, lecture_comp) VALUES ('"+contents[0]+"','"+contents[1]+"',"+contents[2]+",'"+contents[3]+"','"+contents[4]+"','"+contents[5]+"','"+contents[6]+"','"+contents[7]+"',"+contents[2]+",'"+tempLecture[1]+"')")

				if lectureDeleted == False:
					database.query("DELETE FROM subjectlist WHERE coursecode = '"+tempLecture[0]+"' AND section = '"+tempLecture[1]+"'")
					database.query("INSERT INTO subjectlist_lecture (coursecode, section, class_size, time, day, room, pri_instructor, sec_instructor, avail_slots) VALUES ('"+tempLecture[0]+"','"+tempLecture[1]+"',"+tempLecture[2]+",'"+tempLecture[3]+"','"+tempLecture[4]+"','"+tempLecture[5]+"','"+tempLecture[6]+"','"+tempLecture[7]+"',"+tempLecture[2]+")")
					lectureDeleted = True


			else:
				#print("Lecture")
				tempLecture = contents
				lectureDeleted = False
				database.query("INSERT INTO subjectlist (coursecode, section, class_size, time, day, room, pri_instructor, sec_instructor, avail_slots, lecture_comp) VALUES ('"+contents[0]+"','"+contents[1]+"',"+contents[2]+",'"+contents[3]+"','"+contents[4]+"','"+contents[5]+"','"+contents[6]+"','"+contents[7]+"',"+contents[2]+",'None')")

	database.commit()

	database.savetofile()
	print("=================Loading Complete..==================\n")


def loadCatalog():
	catalogs = os.listdir("../CATALOG")


	database.query("CREATE TABLE IF NOT EXISTS catalog (coursecode TEXT, coursename TEXT, units INTEGER)")
	database.commit()

	for entry in catalogs:
		try:
			buf = Parser.fileread("../CATALOG/"+entry)

			details  = buf.split("\n")

			nUnits =  re.search("\((.+)\)", details[1]).group(1)


			database.query("INSERT INTO catalog VALUES ('"+details[0]+"','"+ details[1]+"',"+nUnits+")")

		except:
				print()

	database.commit()

	database.savetofile()

def createSlots():

	filebuf = Parser.fileread("../schedule-list/classlist-2015-1.csv")
	classlist = filebuf.split("\n")
	data = []

	#progress bar
	length = len(classlist)
	interval = int(length / 50)
	string = "Creating Slots: "
	i = 0

	for cls in classlist:

		#progress bar in loop
		if i % interval == 0:
			print(chr(27) + "[2J")
			string = string + "="
			print(string)
		i = i+1

		contents = cls.split(",")


		if len(contents) > 1:

			nAllotment = getNumClassesPerWeek(contents[4])
			d = createData(contents[0]+"-"+contents[1], int(contents[2]) * nAllotment)
			data.append(d)


	mongo_database.addtoCollection("slots", data)

def getAllClasses() :
	buf = database.query("SELECT * FROM subjectlist")

	return buf
def getClass(coursecode):
	buf = database.query("SELECT * FROM subjectlist WHERE COURSECODE = '"+coursecode+"'")

	return buf

def getLecture(coursecode, section):
	buf = database.query("SELECT * FROM subjectlist_lecture WHERE COURSECODE = '"+coursecode+"' AND SECTION = '"+section+"'")

	return buf


def createData(coursecode, classsize):
	slots = []
	for i in range(0, classsize):
		slots.append(i)

	data = {"subjectid":coursecode, "slots": slots}
	return data

def getNumClassesPerWeek(scheduleFormat):
	if scheduleFormat == "WF" or scheduleFormat == "TTh" or scheduleFormat == "MW" or scheduleFormat == "T-F":

		return 2
	elif scheduleFormat == "ThFS":

		return 3
	elif scheduleFormat == "M-S":
		return 6
	else:
		return 1
