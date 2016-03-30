#!/usr/bin/python

from database import Database
from enlister import Enlister

r = Database()

#=========================LOAD INITIAL FILES


#r.loadClasslist()
#r.loadStudentList()


r.loadCurriculum("BSCS-2011-SP-PR")
#Enlister.readCurriculum("BSCS-2011-SP-PR")
