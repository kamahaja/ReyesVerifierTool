from app import app
from app import ValidatorTest as vdt
from flask import render_template, request, flash, redirect, make_response, jsonify, session, url_for
from werkzeug.utils import secure_filename
import json
import time
import os

VERIFIED_FILE_PATH =  "C:/microblog/VERIFIED_FILES"

#view functions go here

@app.route('/', methods = ["GET", "POST"])
@app.route('/index', methods = ["GET", "POST"])
def index():
    if request.method == "POST":

        file = request.files["file"]

        print("File uploaded")
        print(file)

        filename = secure_filename(file.filename)
        file.save(filename)

        res = make_response(jsonify({"message": filename + " uploaded. You will be automatically redirected."}), 200)

        return res
        
    return render_template('index.html')


@app.route('/verify', methods = ['GET', 'POST'])
def verify():
    if request.method == 'POST':
        filetype = request.form.get("selectedHidden", None)
        f = request.files['csvFileInput']
        print(type(f))
        f.save(secure_filename(f.filename))
       
        verifier = vdt.Validator(f.filename, filetype)

        raw_name = os.path.splitext(secure_filename(f.filename))[0]

        flash(verifier.verifyFileToStr())

        if (verifier.verifyFile() == True):
            f.save(os.path.join(VERIFIED_FILE_PATH, raw_name + time.strftime("%Y%m%d-%H%M%S") + ".csv"))

        return redirect(url_for('.index'))
        #return f.filename + ' uploaded successfully'


