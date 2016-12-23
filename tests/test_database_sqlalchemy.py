import unittest
from collections import Counter
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append('../')
from database_setup import Base, Trainer, PoekeBank, Poekemon

import pdb

class DatabaseTest(unittest.TestCase):
	@classmethod
	def setUpClass(self):

		# setup/create database
		self.engine = create_engine('sqlite:///poekebank.db')
		Base.metadata.bind = self.engine

		# session create
		DBSession = sessionmaker(bind=self.engine)
		self.session = DBSession()

	def testHasTables(self):
		keys = Counter(Base.metadata.tables.keys())
		self.assertEquals(keys, Counter(['trainers', 'poekemons', 'poekebank']))
	
	def testInserts(self):
		''' Define some rows for all tables '''
		trainer_names = ['Ash', 'Misty', 'Brock']
		self.session.bulk_insert_mappings(Trainer, [
			dict(
				name= name
			) for name in trainer_names
		])
		self.session.bulk_insert_mappings(Poekemon, [
			dict(
				poekedex_index= name
			) for i in range(10)
		])
		self.session.bulk_insert_mappings(PoekeBank, [
			dict(
				trainer_id= i,
				poekemon_id= i
			) for i in range(3)
		])
		self.session.commit()
		self.assertEquals(self.session.query(Trainer).count(), 3)
		self.assertEquals(self.session.query(Poekemon).count(), 10)
		self.assertEquals(self.session.query(PoekeBank).count(), 3)

	def testQueries(self):
		q = self.session.execute('select * from trainers;')
		rows = q.fetchall()
		self.assertEquals([r[1] for r in rows], ['Ash', 'Misty', 'Brock'])
		# TODO can add more for sure

	def testPokeApiCall(self):
		''' Using PokeApi's call for giving json info of poekemon '''
		q = self.session.execute('select * from poekmons limit 1;')
		poekedex_index = q.first()[1]
		api_url = "https://pokeapi.co/api/v2/pokemon/%s/" %poekedex_index


	@classmethod
	def tearDownClass(self):
		# Clears the DB
		for t in Base.metadata.sorted_tables:
			self.engine.execute(t.delete())

if __name__ == '__main__':
	unittest.main()

