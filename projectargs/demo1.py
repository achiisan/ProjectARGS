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

#MAKE SURE MONGODB IS  RUNNING!

#DEMO1.py
#This script initializes all files (Curricula, Studentlist,Subjects) to database/ projectargs.db


classlist.loadClasslist()
curriculum.loadCurriculumLegacy("curr_test")
studentlist.loadStudentList("PREDICTIONS")
enlister.init()
