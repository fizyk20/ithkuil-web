from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return 'Ithkuil analyzer website under reconstruction.'