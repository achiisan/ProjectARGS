#!/usr/bin/python

import pymongo
from pymongo import MongoClient



def addtoCollection(collection,data):
	post_id = db[collection].insert_many(data)
	
def getSlot(subjectid):
	post_id = db.slots.update({"subjectid": subjectid}, { "$pop" : {"slots": -1}})

	return post_id

client = MongoClient()
db = client.projectargs


def checkSlot(subjectid):
	post_id = db.slots.find({"subjectid": subjectid})	

	for el in post_id:
		return el

