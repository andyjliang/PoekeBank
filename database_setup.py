from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PoekeBank(Base):
	__tablename__ = 'poekebank'
	id = Column(Integer, primary_key=True)
	box = Column(Integer, nullable=True)

	@property 
	def serialize(self):
		return {
			'id': self.id,
			'box': self.box
		}


class Poekemon(Base):
	__tablename__ = 'poekemon'
	id = Column(Integer, primary_key=True)
	poeke_index = Column(Integer, nullable=False)
	# level = Column(Integer, nullable=False)
	# captured_date = Column(Date, nullable=False)
	storage_id = Column(Integer, ForeignKey('poekebank.id'))
	storage = relationship(PoekeBank)

	@property 
	def serialize(self):
		return {
			'id': self.id,
			'poeke_index': self.poeke_index
		}

class Poekedex(Base):
	__tablename__ = 'poekedex'
	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	poketype = Column(String(80), nullable=False)
	evolution_level = Column(Integer)

	@property 
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'poketype': self.poketype,
			'evolution_level': self.evolution_level
		}
		
engine = create_engine('sqlite:///poekebank.db')
Base.metadata.create_all(engine)
print "database created!"