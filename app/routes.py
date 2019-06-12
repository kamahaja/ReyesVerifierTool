from app import app
from app import ValidatorTest as vdt
from flask import render_template

#view functions go here

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/analysis')
def analysis():
    return render_template('index.html')