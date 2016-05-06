#!/usr/bin/python


import curriculum
import classlist
import subjecttree
import studentlist
import mongo_database
import schedulemap
import database

from subjecttree import SubjectTree
from intervaltree import IntervalTree
from schedulemap import ScheduleMap
from tqdm import tqdm

#===========================================
#ENLIST FUNCTION

#GENETIC AND BACKTRACKING ALGO IS CALLED HERE (THey can be created on another file)
currentTerm = 1



def init():



#Implementation should SCAN all curriculum on Database
	buf = curriculum.getCurriculumList()

	for entry in buf:
		for i in range(1,5):
			generateSubjectParseTree(entry[0], i, currentTerm)

	
	for parsetrees in subjecttree.subjecttrees: #String lang napaparse nya dito. Hindi object
		print("Generate a bucket for "+parsetrees)
		subjecttree.subjecttrees[parsetrees].generateBuckets([],1, IntervalTree())
		
		print(len(subjecttree.subjecttrees[parsetrees].buckets))


def enlist():
	#file = open("verbosetester.txt", "w", 1)
	print("ENLISTING...")
	#iterate all parsetrees
	#for parsetrees in subjecttree.subjecttrees:
	#st = subjecttree.subjecttrees["BSCS-2011-SP-PR-4"]
	#get students that is part of that parsetree
	stdlist = studentlist.getAllStudentsByGroup()
	#stdlist = studentlist.getStudentViaCurriculum(st.curriculum,st.year)
	stdlist = stdlist.fetchall()
	pbar = tqdm(total=len(stdlist))
	for student in stdlist:
		#get a student recommended course
		recomm = studentlist.getStudentRecommendedCourses(student[0])
	
		stud = ScheduleMap(student[0])
		courses_list = {}
		#put the recommended courses in a dictionary for easy indexing
		for course in recomm:
			courses_list[course[2]] = 1

		currId = student[4]+"-"+str(student[9])
		
		if currId in subjecttree.subjecttrees:
			#get bucket
			st = subjecttree.subjecttrees[currId]
			if st.bucketcounter < len(st.it_buckets):
				
				bucket = st.it_buckets[st.bucketcounter]

				enlistcompleted = False

				#print("ENLIST = "+student[0]+"\n")
				
				while  enlistcompleted == False:
					
					bucketFailed = False
				#	print("Reset...")

					for item in bucket.items():	
						if item.data.classinfo[0] in courses_list and bucketFailed == False:
							if len(mongo_database.checkSlot(item.data.classinfo[0]+"-"+item.data.classinfo[1])["slots"]) > 0:
								stud.schedule.add(item)
							else:
				#				print("No More Slots on"+item.data.classinfo[0]+" "+item.data.classinfo[1])
								bucketFailed = True
					if bucketFailed == True:
				#		print("Change bucket..")
						st.bucketcounter = st.bucketcounter + 1
						if st.bucketcounter < len(st.it_buckets):
							bucket = st.it_buckets[st.bucketcounter]
							stud.schedule = IntervalTree()
							
						else:
							enlistcompleted = True
					else:
				#		print("Save bucket")
						for item in stud.schedule.items():
							courses_list[item.data.classinfo[0]] = 1
							ret = classlist.getLecture(item.data.classinfo[0],item.data.classinfo[1])
							data = ret.fetchone()

							if data is None:
								studentlist.enlistSection(student[0], item.data.classinfo[0], item.data.classinfo[1])
							
							mongo_database.getSlot(item.data.classinfo[0]+"-"+item.data.classinfo[1])
						enlistcompleted = True
		

		schedulemap.schedules[student[0]] = stud
		
		pbar.update(1)

	pbar.close()		
	
	database.commit()
	database.savetofile()
	printToFileSchedule()
		

def printToFileSchedule():

	print("Writing...")
	buf = curriculum.getCurriculumList()

	for entry in buf:
		curr = entry[0]
		for i in ['1','2','3','4']:
			filename = curr+"-"+i
			file = open(filename, "w", 1)
			sl = studentlist.getStudentViaCurriculum(curr, i)
			for student in sl:
				if student[0] in schedulemap.schedules:
					file.write(schedulemap.schedules[student[0]].studentno+"\n")
					for entry in schedulemap.schedules[student[0]].schedule.items():
						classinfo = entry.data.classinfo
						file.write(classinfo[0]+","+classinfo[1]+","+classinfo[3]+","+classinfo[4]+","+classinfo[5]+","+classinfo[6]+"\n")

						



			
		


def generateSubjectParseTree(curr,year, term): #generate a parse tree given a curriculum and a term


	buf = curriculum.accessCurriculum(curr, year, term)

	temp = SubjectTree(curr, year)

	for entry in buf:

		temp.addClass(entry[0])

	

	subjecttree.subjecttrees[str(curr)+'-'+str(year)] = temp

		
		




