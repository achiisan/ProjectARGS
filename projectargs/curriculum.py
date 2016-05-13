#!/usr/bin/python

from parser import Parser
import database
import re

#Curriculum functions

#Get curriculum from file and save it on (Runtime memory DB and persistent disk DB)

def loadCurriculum(curriculum):

	bfr = Parser.fileread("../Curriculum-list/"+curriculum+".csv")

	semesters = bfr.split("#")
	database.query("CREATE TABLE IF NOT EXISTS curriculum (name TEXT, course TEXT, college TEXT)")
	database.query("CREATE TABLE IF NOT EXISTS '"+curriculum+"' (courseID TEXT PRIMARY_KEY, semester INTEGER, year INTEGER)")
	database.query("CREATE TABLE IF NOT EXISTS '"+curriculum+"-prerequisites' (courseID TEXT, parentcourseID TEXT)")

	parseSemInfo = False

	for semester in semesters:

		#GET SEMESTER INFORMATION
		if(parseSemInfo == False):
			info = semester.split(",")

			database.query("INSERT INTO curriculum VALUES ('"+info[0].strip()+"', '"+info[1].strip()+"', '"+info[2].strip()+"')")
			parseSemInfo = True

		#AFFIX SEMESTER SUBJECTS
		else:
			lists = semester.split("\n") # separate per line
			i = 3
			semInfo = lists[1].split(",") #get contents of FIRST line (semester, year)
			print(semInfo)
			for i in range(2,len(lists)-1): #the succeeding lines determines the subject on that sem and its prerequisites
				info = lists[i].split(",")
				#save subject in DB
				database.query("INSERT INTO '"+curriculum+"' VALUES ('"+info[0]+"', "+semInfo[1]+", "+semInfo[0	]+")")
				for j in range(1, len(info)):
					if(info[j] != ''):
						database.query("INSERT INTO '"+curriculum+"-prerequisites' VALUES ('"+info[j]+"', '"+info[0]+"')")
		print("====END SEMESTER===")

	database.commit()

	database.savetofile()

def loadCurriculumLegacy(curriculum):

	database.query("CREATE TABLE IF NOT EXISTS curriculum (name TEXT, course TEXT, college TEXT)")
	database.commit()

	bfr = Parser.fileread("../Curriculum-list/"+curriculum)

	rem = bfr.split("#####")

	courses = rem[0].split("#")

	for course in courses:
		print("Course")
		print(course)
		gotInfo = False
		lists = course.split("\n")
		for entry in lists:
			info = entry.split(",")
			if len(info) != 1:
				print(entry)
				if gotInfo == False:
					database.query("INSERT INTO curriculum VALUES ('"+info[0].strip()+"', '"+info[2].strip()+"', '"+info[1].strip()+"')")
					database.query("CREATE TABLE IF NOT EXISTS '"+info[0]+"' (courseID TEXT PRIMARY_KEY, semester INTEGER, year INTEGER)")
					gotInfo = True
				else:
						print(info[1])
						if info[1] == "SUBSTITUTION":
							rng = 2
							yrlvl = '-1'
							semester = '-1'
						elif info[1] == "SUMMER":
							rng = 2
							yrlvl = '-1'
							semester = '3'
						else:
							rng =3
							yrlvl = convertYearLevel(info[1])
							semester = convertYearLevel(info[2])


						for i in range(rng,len(info)):
							if info[i] == "ELECTIVE" or info[i] == "GE(AH)" or info[i] == "GE(MST)" or info[i] == "GE(SSP)" or info[i] == "PE 2" or info[i] == "NSTP 1" or info[i] == "NSTP 2" or  re.match(".*\((SSP|MST|AH)\)",info[i]) != None:
								print("")
							else:
								database.query("INSERT INTO '"+info[0]+"' VALUES ('"+info[i]+"', "+semester+", "+yrlvl+")")




	database.commit()
	database.savetofile()

def convertYearLevel(yrlevel):
	if yrlevel == "FIRST":
		return '1'
	if yrlevel == "SECOND":
		return '2'
	if yrlevel == "THIRD":
		return '3'
	if yrlevel == "FOURTH":
		return '4'
	if yrlevel == "SUMMER":
		return '3'
	if yrlevel == "SUBSTITUTION":
		return '0'
	if yrlevel == "FIFTH":
		return '5'
	if yrlevel == "SIXTH":
		return '6'


def accessCurriculum(curr, year ,term):
	print(curr)
	print(year)
	print(term)
	buf = database.query("SELECT * FROM '"+curr+"' WHERE year = "+str(year)+" AND semester = "+str(term))
	return buf

def getCurriculumList():

	buf = database.query("SELECT * FROM curriculum");
	return buf
