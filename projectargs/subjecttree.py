#!/usr/bin/python


import classlist
from intervaltree import IntervalTree
import re


subjecttrees = { }

class SubjectTree:

	def __init__(self, curr, year):
		self.curriculum = curr
		self.year = year
		self.tree = []
		self.height = 0
		self.tree.append(ClassNode(None, self.height, None)) #root node
		#self.buckets = []
		self.it_buckets = []
		self.bucketcounter = 0

	def addClass(self, cls):

		buf = classlist.getClass(cls)

		nextheight = self.height + 1
		leaves = self.getLeaves()

		for node in leaves:
			sections = []
			for entry in buf:
				temp = ClassNode(entry, nextheight, node)
				sections.append(temp)
			self.tree.extend(sections)

		self.height = nextheight

	def getLeaves(self):
		leaves = []

		for node in self.tree:
			if node.height == self.height:
				leaves.append(node)

		return leaves

	def generateBuckets(self,bucket,height, tree): #preorder traversal
			#bucketz = bucket

			hasElements = False
			for elements in self.tree:
				if elements.height == height:

					hasElements = True #yung papasok kasi sa if na ito ay kapag yung height na specified ay nasa current tree pa
					temptree = tree.copy()
					timeframe = calculatetimeframe(elements.classinfo[3], elements.classinfo[4])
					elements.time = timeframe
					hasoverlap = False
					if timeframe != -1:
						for time in timeframe:
							if tree.overlaps(time[0],time[1]) == False:
								tree[time[0]:time[1]] = elements
							else:
								hasoverlap = True

					if hasoverlap == True:

						tree = temptree
						continue
					else:
				#		bucketz.append(elements)
						lecComp = classlist.getLecture(elements.classinfo[0], elements.classinfo[9])
						lectureadded = False

						#if there is a lecture component add it on the schedule
						for entry in lecComp:
							temp = ClassNode(entry,0,None)
							timeframe = calculatetimeframe(entry[3], entry[4])
							temp.time = timeframe
							if timeframe != -1:
								for time in timeframe:
									if tree.overlaps(time[0],time[1]) == False:
										tree[time[0]:time[1]] = temp
									else:
										hasoverlap = True

				#			bucketz.append(temp)
							lectureadded = True

						if hasoverlap == True:
				#			bucketz.pop()
				#			bucketz.pop()
							tree = temptree
							continue

					#recursive function
					ret = self.generateBuckets(bucket, height+1, tree)

				#	get = bucketz.pop()
				#	if lectureadded == True:
				#		get = bucketz.pop()

				#	tree = temptree

			if hasElements == False:
				#self.createBucket(bucketz)
				self.it_buckets.append(tree)
				return 22

	def createBucket(self,bucket):
		self.buckets.append([])
		for elements in bucket:
			self.buckets[len(self.buckets)-1].append(elements)





#####################################################

class ClassNode: #subject node in parse tree (used in subjectree.py)

		def __init__(self, classinfo, height, parent):
			self.classinfo = classinfo
			self.parent = None
			self.height = height
			self.time = None





###################################################
def calculatetimeframe(time, day):

	if time == "TBA"  or day == "TBA":
		return -1
	days = getequivalentDay(day)
	ret = []
	try:
		iterator_day = iter(days)
		for day in days:
			r = []
			d = day*43

			splitted = time.split("-")

			#get lower bound
			splitsecond = splitted[0].split(":")
			hour = milhourLB(splitsecond[0])
			minute = 0
			if len(splitsecond) > 1:
				minute = milmin(splitsecond[1])
			blockid = d+ ((hour-7) * 4) + minute
			#print(blockid)
			r.append(blockid)


			#get upper bound
			splitsecond = splitted[1].strip().split(":")
			hour = milhourUB(splitsecond[0])
			minute = 0

			if len(splitsecond) > 1:
				minute = milmin(splitsecond[1])
			blockid = d+ ((hour-7) * 4) + minute
			#print(blockid)
			r.append(blockid)
			ret.append(r)

		return ret
	except TypeError:
		return -1



def milhourLB(hour):
	if hour == "7":
		return 7
	if hour == "8":
		return 8
	if hour == "9":
		return 9
	if hour == "10":
		return 10
	if hour == "11":
		return 11
	if hour == "12":
		return 12
	if hour == "1":
		return 13
	if hour == "2":
		return 14
	if hour == "3":
		return 15
	if hour == "4":
		return 16
	if hour == "5":
		return 17
	if hour == "6":
		return 18


def milhourUB(hour):

	if hour == "8":
		return 8
	if hour == "9":
		return 9
	if hour == "10":
		return 10
	if hour == "11":
		return 11
	if hour == "12":
		return 12
	if hour == "1":
		return 13
	if hour == "2":
		return 14
	if hour == "3":
		return 15
	if hour == "4":
		return 16
	if hour == "5":
		return 17
	if hour == "6":
		return 18
	if hour == "7":
		return 19
def milmin(minute):

	if minute == "15":
		return 1
	if minute == "30":
		return 2
	if minute == "45":
		return 3


def getequivalentDay(day):
	if day == "Mon":
		return [0]
	if day == "Tues":
		return [1]
	if day == "Wed":
		return [2]
	if day == "Thurs":
		return [3]
	if day == "Fri":
		return [4]
	if day == "Sat":
		return [5]
	if day == "Mon":
		return [0]
	if day == "WF":
		return [2,4]
	if day == "TTh":
		return [1,3]
	if day == "MW":
		return [0,2]
	if day == "M-S":
		return [0,1,2,3,4,5]
	if day == "T-F":
		return [3,4]
	if day == "ThFS":
		return [3,4,5]
	if day == "TBA":
		return []
