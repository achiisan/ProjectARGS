#!/usr/bin/python

from parser import Parser
import database


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

def accessCurriculum(curr, year ,term):
	print(curr)
	print(year)
	print(term)
	buf = database.query("SELECT * FROM '"+curr+"' WHERE year = "+str(year)+" AND semester = "+str(term))
	return buf

def getCurriculumList():
	
	buf = database.query("SELECT * FROM curriculum");
	return buf

