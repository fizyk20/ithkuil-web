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
	word = request.args.get('word', None)
	if not word:
		return redirect(url_for("index"))
	
	try:
		wordObj = fromString(word)
		abbr = wordObj.abbreviatedDescription()
		fullDesc = wordObj.fullDescription()
	except IthkuilException as e:
		return render_template('error.html', errorClass=e.__class__.__name__, errorMsg=str(e))
	
	return render_template("analysis.html", word=wordObj.word, abbr=abbr, fullDesc=fullDesc)

@app.route('/error')
def error():
	return "An error has occured, please return to <a href=\"/\">index</a>"

@app.route('/describe/<code>')
def describe(code):
	from ithkuil.morphology import ithCategValue
	word = request.args.get('word', None)
	catval = Session().query(ithCategValue).filter(ithCategValue.code == code).first()
	return render_template('description.html', categValue=catval, word=word)
	