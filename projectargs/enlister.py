#!/usr/bin/python

from parser import Parser
from curriculum import Curriculum
import database
#===========================================
#ENLIST FUNCTION

#GENETIC AND BACKTRACKING ALGO IS CALLED HERE (THey can be created on another file)

class Enlister:

	@staticmethod
	def generateSchedule():

	#As of now this is configured to
	#run on BSCS-2011-SP-PR curriculum only.

	#Implementation should SCAN all curriculum on Database
		buf = database.accessCurriculum()

		for entry in buf:
			print(entry)

	@staticmethod
	def generateSubjectParseTree(curriculum, term): #generate a parse tree given a curriculum and a term
		print("X")

		
		




