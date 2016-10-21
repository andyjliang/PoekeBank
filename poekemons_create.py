from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Poekemon, PoekeBank

engine = create_engine('sqlite:///poekebank.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

poekebank1 = PoekeBank(box=1)
session.add(poekebank1)
session.commit()

session.add_all([
	Poekemon(poeke_index=25, storage=poekebank1), 
	Poekemon(poeke_index=19, storage=poekebank1),
	Poekemon(poeke_index=21, storage=poekebank1),
	Poekemon(poeke_index=29, storage=poekebank1)
])
session.commit()

print "Created storage box and added several poekemons"