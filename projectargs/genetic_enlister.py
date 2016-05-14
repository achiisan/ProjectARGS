#!/usr/bin/python
import studentlist
import schedulemap
import classlist
import random
import mongo_database
import subjecttree
import enlister
from subjecttree import ClassNode
from intervaltree import IntervalTree


from tqdm import tqdm

subjectpool = {}

#EDIT THIS PARAMETERS

nGenerations = 10
perCrossover = 85
perMutate = 100 - perCrossover
nTrials = 50

def generateSubjectPool():
	buf = classlist.getAllClasses()

	for entry in tqdm(buf):
		if entry[0] in subjectpool:
			subjectpool[entry[0]].append(entry)
		else:
			subjectpool[entry[0]] = []


def enlist():
	stdlist = studentlist.getAllStudentsByGroup()
	file = open("test.txt", "w",1)
	listed = stdlist.fetchall()

	for student in tqdm(listed):
		treshold = 1.0
		specieHighestScorer = None



		if student[0] in schedulemap.schedules:

			sched = schedulemap.schedules[student[0]]
			recomm = studentlist.getStudentRecommendedCourses(student[0])
			maxUnits = studentlist.getStudentMaxUnits(student[0])
			currUnits = 0
			trials = 0
			candidatesubjs = []
			minischedules = []

			#print(student[0])
			#file.write(student[0]+"\n")
			#print(maxUnits)

			#get recommended courses and separated enlisted and not enlisted subjects
			for entry in recomm:
				if entry[3] is not "":
					#file.write(entry[0]+entry[1]+entry[2]+entry[3]+"\n")
					currUnits = currUnits + int(entry[4])
				else:
					candidatesubjs.append(entry)

			#geenrate population (set of random sections)
			for i in range(0,nGenerations):
				ms = miniSchedule()
				ms.tree = sched.schedule.copy()
				ms.nunits = currUnits

				for entry in candidatesubjs:
					if ms.nunits + int(entry[4]) >= maxUnits:
						break

					if entry[2] in subjectpool and len(subjectpool[entry[2]]) > 0:
						k = random.choice(subjectpool[entry[2]])

						ms.generation.append(k)
						ms.nunits = ms.nunits + int(entry[4])


				minischedules.append(ms)

			#score each population and get the highest score
			for j in minischedules:
				for k in j.generation:

					if len(mongo_database.checkSlot(k[0]+"-"+k[1])["slots"]) <= 0:
						j.score = j.score - 0.2
					else:
						timeframe = subjecttree.calculatetimeframe(k[3],k[4])
						if timeframe != -1:
							for time in timeframe:
								if j.tree.overlaps(time[0], time[1]) == True:
									j.score = j.score - 0.1
								else:
									j.tree[time[0]:time[1]] = ClassNode(k,0,None)

					lecComp = classlist.getLecture(k[0], k[9])
					for entry in lecComp:
						if len(mongo_database.checkSlot(entry[0]+"-"+entry[1])["slots"]) <= 0:
							j.score = j.score - 0.2
						else:
							timeframe = subjecttree.calculatetimeframe(entry[3],entry[4])
						if timeframe != -1:
							for time in timeframe:
								if j.tree.overlaps(time[0], time[1]) == True:
									j.score = j.score - 0.1
								else:
									j.tree[time[0]:time[1]] = ClassNode(entry,0,None)

				if specieHighestScorer == None:
					specieHighestScorer = j
				else:
					if specieHighestScorer.score < j.score:
						specieHighestScorer = j

			#if specieHighestScorer.score >= treshold:
			sched.schedule = specieHighestScorer.tree
			for item in sched.schedule.items():
				ret = classlist.getLecture(item.data.classinfo[0],item.data.classinfo[1])
				data = ret.fetchone()

				if data is None:
					studentlist.enlistSection(student[0], item.data.classinfo[0], item.data.classinfo[1])

#			else:
#				while trials < nTrials:
#					trials = trials + 1
#					candidate = crossover(sched.schedule,specieHighestScorer,random.choice(minischedules))
#					for generated in candidate:
#						if generated.score > specieHighestScorer.score:
#							specieHighestScorer = generated

#					if specieHighestScorer.score >= treshold:
#						trials = nTrials





	enlister.printToFileSchedule()
	database.commit()
	database.savetofile()



def crossover(initialSched,sched1,sched2):

	child1 = miniSchedule()
	child1.tree = initialSched.copy()

	child2 = miniSchedule()
	child2.tree = initialSched.copy()


	children = [child1, child2]

	cutpoint = int(len(sched1.generation)/2)

	x0 = sched1.generation[0:cutpoint]
	x1 = sched1.generation[cutpoint:len(sched1.generation)]

	y0 = sched2.generation[0:cutpoint]
	y1 = sched2.generation[cutpoint:len(sched2.generation)]

	children[0].generation = x0+y1
	children[1].generation = y0+x1

	for j in children:
		for k in j.generation:

			if len(mongo_database.checkSlot(k[0]+"-"+k[1])["slots"]) <= 0:
						j.score = j.score - 0.2
			else:
				timeframe = subjecttree.calculatetimeframe(k[3],k[4])
				if timeframe != -1:
					for time in timeframe:
						if j.tree.overlaps(time[0], time[1]) == True:
							j.score = j.score - 0.1
						else:
							j.tree[time[0]:time[1]] = ClassNode(k,0,None)

			lecComp = classlist.getLecture(k[0], k[9])
			for entry in lecComp:
				if len(mongo_database.checkSlot(entry[0]+"-"+entry[1])["slots"]) <= 0:
					j.score = j.score - 0.2
				else:
					timeframe = subjecttree.calculatetimeframe(entry[3],entry[4])
				if timeframe != -1:
					for time in timeframe:
						if j.tree.overlaps(time[0], time[1]) == True:
							j.score = j.score - 0.1
						else:
							j.tree[time[0]:time[1]] = ClassNode(entry,0,None)

	return children

def mutate(sched1):
	print("Y")
##########################################
class miniSchedule:

	def __init__(self):
		self.score = 1
		self.nunits = 0
		self.generation = []
		self. tree = None
