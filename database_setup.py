from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Trainer(Base):
	__tablename__ = 'trainers'
	# __table_args__ = {'sqlite_autoincrement': True}
	trainer_id = Column(Integer, autoincrement=True, primary_key=True)
	name = Column(String, nullable=True)
	sqlite_autoincrement=True

	@property 
	def serialize(self):
		return {
			'trainer_id': self.trainer_id,
			'name': self.name
		}

class Poekemon(Base):
	__tablename__ = 'poekemons'
	# __table_args__ = {'sqlite_autoincrement': True}
	poekemon_id = Column(Integer, autoincrement=True, primary_key=True)
	poekedex_index = Column(String, nullable=True)

	@property 
	def serialize(self):
		return {
			'poekemon_id': self.poekemon_id,
			'poekedex_index': self.poekedex_index
		}

class PoekeBank(Base):
	__tablename__ = 'poekebank'
	poekemon_id = Column(Integer, ForeignKey('poekemons.poekemon_id'), primary_key=True)
	trainer_id = Column(Integer, ForeignKey('trainers.trainer_id'))

	@property 
	def serialize(self):
		return {
			'poekemon_id': self.poekemon_id,
			'trainer_id': self.trainer_id
		}

	
engine = create_engine('sqlite:///poekebank.db')
Base.metadata.create_all(engine)
print "database created!"