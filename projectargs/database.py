#!/usr/bin/python

import redis
from parser import  Parser

class Database:

		def __init__(self):
			self.r = redis.StrictRedis(host='localhost', port=6379, db=0)


		def loadClasslist(self):
			filebuf = Parser.fileread("../schedule-list/classlist-2015-1.csv")
			classlist = filebuf.split("\n")
			

			for cls in classlist:
				self.r.incr('subjcount')
				n = self.r.get('subjcount')

				contents = cls.split(",")
				mapping = {'coursecode':contents[0], 'section': contents[1], 'class_size': contents[2],'time':contents[3],'day': contents[4], 'room': contents[5], 'pri_instructor': contents[6], 'sec_instructor':contents[7]}

				self.r.sadd('subjectlist',self.r.hmset('subject:'+str(n),mapping))

				
				
					
				





		




		







