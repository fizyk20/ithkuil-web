from flask import Flask, render_template, request, redirect, url_for
from ithkuil.morphology.exceptions import IthkuilException

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/analyze')
def analyze():
	from ithkuil.morphology import fromString
	
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