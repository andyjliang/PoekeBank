import unittest
import psycopg2
# Implemented with PostgresSQL 
import sys
sys.path.append('../')

class DatabaseTest(unittest.TestCase):

	def setup(self):
		'''	Open connection to psql, create poekemon database '''
		psql_file = open('poekebank.sql','r').read()
		self.connection = connect('dbname=poekebank')
		self.connection.cursor(psql_file)

		# test
		print 

	def testBaseStructure(self):
		pass

	def testReferences(self):
		pass

	def testPokeAPI(self):
		pass

	def tearDown(self):
		''' Close psql connection and drop poekebank database'''
		self.connection.close()

if '__name__' == '__main__':
	unittest.main()