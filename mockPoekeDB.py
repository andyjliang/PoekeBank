from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, PoekeBank, Poekemon, Trainer
from random import randint, shuffle

engine = create_engine('sqlite:///poekebank.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

#reset database 
# for table in Base.metadata.sorted_tables:
# 	engine.execute(table.delete())
# session.execute("update sqlite_sequence set seq = 0 where name='trainers'; ")


poekemon_list = [randint(1,100) for i in range(30)]
trainers = ['Ash', 'Misty', 'Brock']
session.bulk_insert_mappings(Trainer, [
	dict(
		name = name
	) for name in trainers
])
session.bulk_insert_mappings(Poekemon, [
	dict(
		poekedex_index = pind
	) for pind in poekemon_list
])
n_range = range(30)
shuffle(n_range)
session.bulk_insert_mappings(PoekeBank, [
	dict(
		trainer_id = randint(1,3),
		poekemon_id = n_range.pop()
	) for i in range(10)
])
session.commit()