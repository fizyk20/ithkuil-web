from flask import Flask, render_template, request, redirect, url_for
from ithkuil.morphology.exceptions import IthkuilException
from ithkuil.morphology.data import ithCategValue
from ithkuil.morphology import Session, fromString

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/analyze')
def analyze():
	text = request.args.get('text', None)
	if not text:
		return redirect(url_for("index"))
	
	data = []
	
	try:
		words = text.replace('.',' ').replace(',',' ').replace('!',' ').replace('?',' ').lower().split()
		previousCarrier = False		# remembers if the previous word had a carrier root
		for word in words:
			if not previousCarrier:
				wordObj = fromString(word)
				abbr = wordObj.abbreviatedDescription()
				fullDesc = wordObj.fullDescription()
				if 'Cr' in wordObj.slots and wordObj.slots['Cr'] == 'p':
					previousCarrier = True
				data.append({ 'word': wordObj.word, 'abbr': abbr, 'full': fullDesc })
			else:
				data.append({ 'word': word, 'abbr': '"Carried" word' })
				previousCarrier = False
	except IthkuilException as e:
		return render_template('error.html', errorClass=e.__class__.__name__, errorMsg=str(e))
	
	return render_template("analysis.html", text=text, data=data)

@app.route('/error')
def error():
	return "An error has occured, please return to <a href=\"/\">index</a>"

@app.route('/describe/<code>')
def describe(code):
	text = request.args.get('text', None)
	catval = Session().query(ithCategValue).filter(ithCategValue.code == code).first()
	return render_template('description.html', categValue=catval, text=text)
	