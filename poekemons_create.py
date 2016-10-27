from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Poekemon, PoekeBank, Poekedex

engine = create_engine('sqlite:///poekebank.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

poekebank1 = PoekeBank(box=1)
session.add(poekebank1)
session.commit()

session.add_all([
	Poekemon(poeke_index=1, storage=poekebank1), 
	Poekemon(poeke_index=3, storage=poekebank1),
	Poekemon(poeke_index=7, storage=poekebank1),
	Poekemon(poeke_index=12, storage=poekebank1)
])
session.add_all([
	Poekedex(name="Bulbasaur", poketype="Grass/Poison", evolution_level=16), 
	Poekedex(name="Ivysaur", poketype="Grass/Poison", evolution_level=32),
	Poekedex(name="Venusaur", poketype="Grass/Poison"),
	Poekedex(name="Charmander", poketype="Fire", evolution_level=16),
	Poekedex(name="Charmeleon", poketype="Fire", evolution_level=32),
	Poekedex(name="Charizard", poketype="Fire/Flying"),
	Poekedex(name="Squirtle", poketype="Water", evolution_level=16),
	Poekedex(name="Wartortle", poketype="Water", evolution_level=32),
	Poekedex(name="Blastoise", poketype="Water"),
	Poekedex(name="Caterpie", poketype="Bug", evolution_level=7),
	Poekedex(name="Metapod", poketype="Bug", evolution_level=10),
	Poekedex(name="Butterfree", poketype="Bug/Flying")
])
session.commit()

print "Created storage box and added several poekemons"