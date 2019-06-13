from app import app
from app import ValidatorTest as vdt
from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename

#view functions go here

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/verify', methods = ['GET', 'POST'])
def verify():
    if request.method == 'POST':
        if 'csvFileInput' not in request.files:
            flash('No file part')
            return render_template('index.html')
        file = request.files['csvFileInput']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return render_template('index.html')
        f = request.files['csvFileInput']
        f.save(secure_filename(f.filename))
        return render_template('index.html', output = vdt.verifyFileToStr())
        #return f.filename + ' uploaded successfully'
