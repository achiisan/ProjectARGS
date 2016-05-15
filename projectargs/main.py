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
#curriculum.loadCurriculumLegacy("TAMACURRICULA-2014-FIRST")
#curriculum.loadCurriculumLegacy("curr_test")
#studentlist.loadStudentList(PREDICTIONS)


########################################################
#Enlisting functions here

classlist.createSlots()
#enlister.init()
enlister.loadBuckets()

enlister.enlist()

genetic_enlister.generateSubjectPool()
genetic_enlister.enlist()
