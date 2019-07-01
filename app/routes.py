from app import app
from app import ValidatorTest as vdt
from flask import render_template, request, flash, redirect, make_response, jsonify, session, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
from shutil import copyfile
from datetime import datetime
from tabulate import tabulate
import json
import time
import os

# GOAL FOR 6/27
# create VerifiedFile class to store the date uploaded of each file on creation
# so that we can sort the verified files by date

# OR use os modules to append creation dates to the filename and
# sort them that way


APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 

VERIFIED_FILE_PATH = os.path.join(APP_ROOT, 'VERIFIED_FILES')

JSON_FILE_PATH = "app/formatSettings.json"

def numPreviousUploads(fileName):
    listOfFiles = os.listdir(VERIFIED_FILE_PATH)
    count = 0
    for file in listOfFiles:
        if fileName in file:
            count = count + 1

    return count

def stripExtension(fileName):
    return os.path.splitext(fileName)[0]

def stripDate(fileNameWithDate):
    return fileNameWithDate.rsplit("_", 1)[0]

def dateUploaded(fileName):
    raw_name = stripExtension(fileName)

    raw_date = raw_name.rsplit("_", 1)[1]

    myTime = datetime.strptime(raw_date, "%Y%m%d-%H%M%S")

    return myTime.strftime("%m/%d/%Y -- %H:%M:%S")
    


#view functions go here

@app.route('/', methods = ["GET", "POST"])
@app.route('/index', methods = ["GET", "POST"])
def index():
    if request.method == "POST":

        file = request.files["file"]
        fileType = request.form.get("fileTypeData")

        print("File uploaded")
        print(file)

        filename = secure_filename(file.filename)
        file.save(filename)

        print(filename)
        verifier = vdt.Validator(filename, fileType, JSON_FILE_PATH)

        raw_name = os.path.splitext(filename)[0]

        #create end string
        output = verifier.verifyFileToStr()
        if (numPreviousUploads(raw_name) > 0):
            output += "<br>" + filename + " has " + str(numPreviousUploads(raw_name)) + " previously verified version(s). Check the history tab to view/download previous versions."
        else:
            output += "<br>" + filename + " has never been verified."

        verified = verifier.verifyFile()
        #raw_name + time.strftime("%Y%m%d-%H%M%S") + ".csv"
        if (verified == True):
            copyfile(filename, VERIFIED_FILE_PATH + "/" + raw_name + "_" + time.strftime("%Y%m%d-%H%M%S") + ".csv")

        os.remove(filename)
        
        res = make_response(jsonify({"message": output, "valid": verified}), 200)

        return res
        
    return render_template('index.html')

def getFileType(fileName):
    if "sales" in fileName.lower():
        return "Sales"
    if "payroll" in fileName.lower():
        return "Payroll"
    if "sales" in fileName.lower():
        return "Sales"
    if "static percentage" or "static_percentage" in fileName.lower():
        return "Static Percentages"

def getCoID(fileName):
    if "FDC" in fileName:
        return "FDC"
    if "FGC" in fileName:
        return "FGC"
    if "HJL" in fileName:
        return 'HJL'

@app.route('/history')
def history():
    listOfFiles = os.listdir(VERIFIED_FILE_PATH)
    output=""
    for file in listOfFiles:
        raw_name = stripExtension(file)
        raw_name = stripDate(raw_name)
        fileType = getFileType(raw_name)
        coID = getCoID(raw_name)
        date = dateUploaded(file)
        output = ("<tr><td><a href= '/uploads/VERIFIED_FILES/" + file + "'>" + raw_name + "</a></td>" +
        "<td>" + coID + "</td>" +
        "<td>" + fileType + "</td>" + 
        "<td>User</td>" + 
        "<td>" + date + "</td>" + 
        "</tr>")
        flash(output)
    
    return render_template('history.html')

@app.route("/uploads/<path:file_name>", methods = ['GET', 'POST'])
def download(file_name):
    try:
        #return("Hello")
        return send_from_directory(APP_ROOT, file_name, as_attachment=True)
        #return send_file(APP_ROOT + file_name, as_attachment=True)
    except Exception as e:
        return str(e)

@app.route("/settings", methods = ["GET", "POST"])
def settings():
    if request.method == "POST":
        #use the request object to get the file from the file input in index.html
        jsonFile = request.files['jsonFileInput']

        filename = secure_filename(jsonFile.filename)

        print(filename)
        jsonFile.save(JSON_FILE_PATH)
    
        return ('', 204)

    flash("<a href= '/uploads/formatSettings.json'>Current Settings File</a>")
    return render_template("settings.html")

