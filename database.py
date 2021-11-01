import pymongo
import os

class Database:
	DB=None

	@staticmethod
	def initialize():
		client=pymongo.MongoClient(os.environ['MONGOLAB_URI'])
		Database.DB=client.mydb


	@staticmethod
	def insert_record(doc):
		Database.DB.entries.insert(doc)

	@staticmethod
	def get_records():
		return [x for x in Database.DB.entries.find({})]

	@staticmethod
	def delete_all_records():
		Database.DB.entries.remove({})