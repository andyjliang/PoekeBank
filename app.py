from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Poekemon, PoekeBank, Poekedex

app = Flask(__name__)
engine = create_engine('sqlite:///poekebank.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/poekebanks/')
def showPoekebanks():
	poekedex = session.query(Poekedex).all()
	poekebanks = session.query(PoekeBank).all()
	poekemons = session.query(Poekemon).all()
	return render_template('poekebanks.html', poekebanks=poekebanks, poekemons=poekemons, poekedex=poekedex)

@app.route('/poekebanks/JSON')
def poekebanksJSON():
	poekebanks = session.query(PoekeBank).all()
	return jsonify(poekebanks=[p.serialize for p in poekebanks])

@app.route('/poekebanks/new/', methods=['GET', 'POST'])
def newPoekeBank():
	if request.method == 'POST':
		newPoekeBank = PoekeBank(box=request.form['box'])
		session.add(newPoekeBank)
		session.commit()
		return redirect(url_for('showPoekebanks'))
	else:
		return render_template('newPoekebanks.html')

@app.route('/poekebanks/<int:poekebank_id>/edit/', methods=['GET', 'POST'])
def editPoekeBank(poekebank_id):
	editedPoekeBank = poekebank = session.query(PoekeBank).filter_by(id=poekebank_id).one()
	if request.method == "POST" and request.form['box']:
		editedPoekeBank.box = request.form['box']
		return redirect(url_for('showPoekebanks'))
	else:
		return render_template('editPoekebank.html', poekebank=editedPoekeBank)

@app.route('/poekebanks/<int:poekebank_id>/delete/', methods=['GET', 'POST'])
def deletePoekeBank(poekebank_id):
	poekeBankToDelete = session.query(PoekeBank).filter_by(id=poekebank_id).one()
	if request.method == "POST":
		session.delete(poekeBankToDelete)
		session.commit()
		return redirect(url_for('showPoekebanks', poekebank_id=poekebank_id))
	else:
		return render_template('deletePoekebank.html', poekebank=poekeBankToDelete)


@app.route('/poekebanks/<int:poekebank_id>/')
@app.route('/poekebanks/<int:poekebank_id>/poekemon')
def showPoekemons(poekebank_id):
	poekebank = session.query(PoekeBank).filter_by(id=poekebank_id).one()
	poekemons = session.query(Poekemon, Poekedex).filter(Poekemon.poeke_index==Poekedex.id).filter_by(storage_id=poekebank_id).all()
	return render_template('poekemons.html', poekebank=poekebank, poekemons=poekemons)

@app.route('/poekebanks/<int:poekebank_id>/poekemon/JSON')
def poekeBankPoekemonJSON(poekebank_id):
	poekebank = session.query(PoekeBank).filter_by(id=poekebank_id).one()
	poekemons = session.query(Poekemon).filter_by(storage_id=poekebank_id).all()
	return jsonify(poekemons=[p.serialize for p in poekemons])

@app.route('/poekebanks/<int:poekebank_id>/poekemon/new/', methods=['GET', 'POST'])
def newPoekemon(poekebank_id):
	poekebank = session.query(PoekeBank).filter_by(id=poekebank_id).one()
	if request.method == 'POST':
		if session.query(func.count(poekebank.id)) <= 5:
			newPoekemon = Poekemon(poeke_index=request.form['poeke_index'], storage=poekebank)
			session.add(newPoekemon)
			session.commit()
		else:
			print "box storage amount exceeded"
		return redirect(url_for('showPoekemons', poekebank_id=poekebank_id))
	else:
		return render_template('newPoekemon.html', poekebank_id=poekebank_id)


@app.route('/poekebanks/<int:poekebank_id>/poekemon/<int:poekemon_id>/edit/', methods=['GET', 'POST'])
def editPoekemon(poekebank_id, poekemon_id):
	editedPoekemon = session.query(Poekemon).filter_by(id=poekemon_id).one()
	if request.method == 'POST':
		if request.form['poeke_index']:
			editedPoekemon.poeke_index = request.form['poeke_index']
		session.add(editedPoekemon)
		session.commit()
		return redirect(url_for('showPoekemons', poekebank_id=poekebank_id))
	else:
		return render_template('editPoekemon.html', poekebank_id=poekebank_id, poekemon_id=poekemon_id, poekemon=editedPoekemon)

@app.route('/poekebanks/<int:poekebank_id>/poekemon/<int:poekemon_id>/delete/', methods=['GET', 'POST'])
def deletePoekemon(poekebank_id, poekemon_id):
	poekemonToDelete = session.query(Poekemon).filter_by(id=poekemon_id).one()
	if request.method == "POST":
		session.delete(poekemonToDelete)
		session.commit()
		return redirect(url_for('showPoekemons', poekebank_id=poekebank_id))
	else:
		return render_template('deletePoekemon.html', poekebank_id=poekebank_id, poekemon=poekemonToDelete)


@app.route('/poekebanks/<int:poekebank_id>/poekemon/<int:poekemon_id>/JSON')
def poekemonJSON(poekebank_id, poekemon_id):
	poekebank = session.query(PoekeBank).filter_by(id=poekebank_id).one()
	poekemons = session.query(Poekemon).filter_by(storage_id=poekebank_id).all()
	return jsonify(Poekemons=[p.serialize for p in poekemons])


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)