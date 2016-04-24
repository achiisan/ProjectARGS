#!/usr/bin/python

import database
import classlist
import studentlist
import curriculum
import enlister
import subjecttree
from intervaltree import IntervalTree


#=========================LOAD INITIAL FILES


#classlist.loadClasslist()
#curriculum.loadCurriculum("BSCS-2011-SP-PR")
#studentlist.loadStudentList()


########################################################
#Enlisting functions here


enlister.init()
enlister.enlist()

