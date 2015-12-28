from flask import Flask, render_template, request, redirect, url_for

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
	
	wordObj = fromString(word)
	abbr = wordObj.abbreviatedDescription()
	
	return render_template("analysis.html", word=word, abbr=abbr)

@app.route('/error')
def error():
	return "An error has occured, please return to <a href=\"/\">index</a>"