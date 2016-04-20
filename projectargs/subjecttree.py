#!/usr/bin/python


import classlist



subjecttrees = { }

class SubjectTree:

	def __init__(self, curr, term):
		self.curriculum = curr
		self.term = term
		self.tree = []
		self.height = 0
		self.tree.append(ClassNode(None, self.height, None)) #root node
		self.buckets = []
		



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

		print("Added all Sections of "+cls)



	def getLeaves(self):
		leaves = []

		for node in self.tree:
			if node.height == self.height:
				leaves.append(node)

		return leaves

	def generateBuckets(self,bucket,height): #preorder traversal
			bucketz = bucket

			hasElements = False
			for elements in self.tree:
				if elements.height == height:
					hasElements = True
					bucketz.append(elements)
					ret = self.generateBuckets(bucketz, height+1)
					bucketz.pop()

					#print("Add to buckets!")
					
			if hasElements == False:
				self.createBucket(bucketz)
				return 22

	def createBucket(self,bucket):
		self.buckets.append([])
	#	print("Create bucket:")
		for elements in bucket:
	#		print(elements.classinfo)
			self.buckets[len(self.buckets)-1].append(elements)
	


	
#####################################################

class ClassNode: #subject node in parse tree (used in subjectree.py)

		def __init__(self, classinfo, height, parent):
			self.classinfo = classinfo
			self.parent = None
			self.height = height









