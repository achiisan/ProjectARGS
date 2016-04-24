#!/usr/bin/python


import curriculum
import classlist
import subjecttree
import studentlist

from subjecttree import SubjectTree
from intervaltree import IntervalTree

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
		
		#for k in subjecttree.subjecttrees[parsetrees].it_buckets:
		#	print("Bucket:")
		#	for interval_object in k:
		#		print(interval_object.data.classinfo)

		print(len(subjecttree.subjecttrees[parsetrees].buckets))


def enlist():
	buf = curriculum.getCurriculumList()

	for parsetrees in subjecttree.subjecttrees:
		st = subjecttree.subjecttrees[parsetrees]
		stdlist = studentlist.getStudentViaCurriculum(st.curriculum, st.year)
		for student in stdlist:
			
			recomm = studentlist.getStudentRecommendedCourses(student[0])
			for course in recomm:
				print(course)



			
		


def generateSubjectParseTree(curr,year, term): #generate a parse tree given a curriculum and a term


	buf = curriculum.accessCurriculum(curr, year, term)

	temp = SubjectTree(curr, year)

	for entry in buf:
		temp.addClass(entry[0])

	print("===END PARSE TREE===");

	subjecttree.subjecttrees[str(curr)+'-'+str(year)] = temp

		
		




