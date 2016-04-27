#!/usr/bin/python

import database
import classlist
import studentlist
import curriculum
import enlister
import subjecttree
import mongo_database
from intervaltree import IntervalTree


#=========================LOAD INITIAL FILES


#classlist.loadClasslist()
#curriculum.loadCurriculum("BSCS-2011-SP-PR")
#studentlist.loadStudentList()


########################################################
#Enlisting functions here

classlist.createSlots()

enlister.init()
enlister.enlist()


#ret = mongo_database.getSlot("AEC 1-T-4R")
	#if ret["nModified"] == 0 or ret["updatedExisting"] == False:
	#	print("No Records to Modify.")
	#	break

