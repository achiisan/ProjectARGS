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
#This script runs the backtracking and genetic enlisters

#Enlisting functions here

classlist.createSlots()
enlister.loadBuckets()

enlister.enlist()

genetic_enlister.generateSubjectPool()
genetic_enlister.enlist()
