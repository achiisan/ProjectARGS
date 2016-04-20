#!/usr/bin/python


import curriculum
import classlist
import subjecttree

from subjecttree import SubjectTree

#===========================================
#ENLIST FUNCTION

#GENETIC AND BACKTRACKING ALGO IS CALLED HERE (THey can be created on another file)
currentTerm = 1



def generateSchedule():

#As of now this is configured to
#run on BSCS-2011-SP-PR curriculum only.

#Implementation should SCAN all curriculum on Database
	buf = curriculum.getCurriculumList()

	for entry in buf:
		for i in range(1,5):
			generateSubjectParseTree(entry[0], i, currentTerm)

	
	for parsetrees in subjecttree.subjecttrees: #String lang napaparse nya dito. Hindi object
		print("Generate a bucket for "+parsetrees)
		subjecttree.subjecttrees[parsetrees].generateBuckets([],1)
		
		for k in subjecttree.subjecttrees[parsetrees].buckets:
			print("Bucket:")
			for elements in k:
				print(elements.classinfo)

		print(len(subjecttree.subjecttrees[parsetrees].buckets))
			
		


def generateSubjectParseTree(curr,year, term): #generate a parse tree given a curriculum and a term


	buf = curriculum.accessCurriculum(curr, year, term)

	temp = SubjectTree(curr, term)

	for entry in buf:
		temp.addClass(entry[0])

	print("===END PARSE TREE===");

	subjecttree.subjecttrees[str(curr)+'-'+str(year)] = temp

		
		




