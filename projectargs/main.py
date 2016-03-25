#!/usr/bin/python

from database import Database


r = Database()

#=========================LOAD INITIAL FILES
r.loadClasslist()
r.loadStudentList()

