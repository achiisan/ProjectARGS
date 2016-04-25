#!/usr/bin/python

from intervaltree import IntervalTree
#Class for a schedule of a student

schedules = { }

class ScheduleMap:

	def __init__(self, studentno):
		self.schedule = IntervalTree()
		self.studentno = studentno

	def enlistFromBucket(bucket):
		print("X")
		