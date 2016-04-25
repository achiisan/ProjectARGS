#!/usr/bin/python

import pymongo
from pymongo import MongoClient



def addtoCollection(collection,data):
	post_id = db[collection].insert_many(data)
	
def getSlot(subjectid):
	post_id = db.slots.update({"subjectid": subjectid}, { "$pop" : {"slots": -1}})

	print(post_id)

	return post_id

client = MongoClient()
db = client.projectargs

