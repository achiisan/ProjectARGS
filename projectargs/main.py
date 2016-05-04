#!/usr/bin/python

import database
import classlist
import studentlist
import curriculum
import enlister
import subjecttree
import mongo_database
import genetic_enlister
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
genetic_enlister.generateSubjectPool()
genetic_enlister.enlist()


