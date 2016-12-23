-- create database poekebank;

create table trainer(
	trainer_id serial primary key,
	name varchar(30) 
);

create table poekemon(
	poekemon_id serial primary key,
	poekedex_index integer
);

create table poekebank(
	poekemon_id integer references poekemon(poekemon_id),
	trainer_id integer references trainer(trainer_id)
);