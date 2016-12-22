import unittest
from collections import Counter
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Poekemon, PoekeBank, Poekedex


class DBTest(unittest.TestCase):
	def setup(self):
		engine = create_engine('sqlite:///poekebank.db')
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()

	def testHasRightTables(self):
		self.assertTrue(Counter(Base.metadata.tables.keys()), Counter(['poekemon', 'poekedex', 'poekebank']))
		

if __name__ == '__main__':
	unittest.main()
