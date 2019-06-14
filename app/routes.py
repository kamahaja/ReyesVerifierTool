from app import app
from app import ValidatorTest as vdt
from flask import render_template, request, flash, redirect, make_response, jsonify
from werkzeug.utils import secure_filename

#view functions go here

@app.route('/', methods = ["GET", "POST"])
@app.route('/index', methods = ["GET", "POST"])
def index():
    if request.method == "POST":

        file = request.files["file"]

        print("File uploaded")
        print(file)

        filename = secure_filename(file.filename)

        res = make_response(jsonify({"message": filename + " uploaded"}), 200)

        return res
        
    return render_template('index.html')


@app.route('/verify', methods = ['GET', 'POST'])
def verify():
    if request.method == 'POST':
        if 'csvFileInput' not in request.files:
            flash('No file part')
            return render_template('index.html')
        file = request.files['csvFileInput']
        filetype = request.form.get("selectedHidden", None)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '' or filetype == None or filetype == "":
            flash('Invalid file or type!')
            return render_template('index.html')
        f = request.files['csvFileInput']
        f.save(secure_filename(f.filename))
        return render_template('index.html', output = vdt.verifyFileToStr(f.filename, filetype))
        #return f.filename + ' uploaded successfully'
