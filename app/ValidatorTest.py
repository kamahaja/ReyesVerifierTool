import pandas as pd
import numpy as np
import datetime

INVENTORY_LABELS = ["CoID", "Date", "CostCtr", "SHRINKAGE_QTY", "SHRINKAGE_AMT", "BREAKAGE_QTY", "BREAKAGE_AMT", "OVERAGE_QTY", "OVERAGE_AMT"]
SALES_LABELS = ["CoID", "Date", "CostCtr", "Ces", "Stops", "GP Dollars"]
PAYROLL_LABELS = ["CoID", "Date", "CostCtr", "ProdHrs", "OTHrs", "ProdDollars", "Headcount"]
STATIC_PERCENTAGES_LABELS = ["CoID", "Date", "CostCtr", "SBT", "RET", "UNS", "SPE"]

def parseCSV(filename):
    df = pd.read_csv(filename, dtype='str') #we want strings because some are not ints
    df.columns = df.columns.str.strip()
    if df.isnull().values.any():  #if there are empty cells it will not work
        return None
    dict = df.to_dict(orient='list')
    return dict

def checkLabels(dict, fileType):
    areLabelsCorrect = False
    if (fileType.lower() == "inventory"):
        areLabelsCorrect = list(dict.keys()) == INVENTORY_LABELS
    elif (fileType.lower() == "sales"):
        areLabelsCorrect = list(dict.keys()) == SALES_LABELS
    elif (fileType.lower() == "payroll"):
        areLabelsCorrect = list(dict.keys()) == PAYROLL_LABELS
    else:
        areLabelsCorrect = list(dict.keys()) == STATIC_PERCENTAGES_LABELS

    print("Labels are verified: " + str(areLabelsCorrect))
    return areLabelsCorrect

def validateDateFormat(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m/%d/%Y')
        return True
    except ValueError:
        return False
        #raise ValueError("Incorrect data format, should be MM-DD-YYYY")

def checkDates(dict):
    print("Checking dates")
    for date in dict["Date"]:
        if validateDateFormat(date) == False:
            return False
    
    print("Dates are verified")
    return True

def hasNumber(inputString):
    return any(char.isdigit() for char in inputString)

def checkIds(dict):
    print("Checking ids")
    for index, company in enumerate(dict["CoID"]):
        if hasNumber(company) or len(company) < 3:
            print("Invalid company id on row " + str(index + 2) + ": " + company)
            return False
    
    print("IDs are verified.")
    return True

def checkCosts(dict):
    print("Checking costs")
    for index, cost in enumerate(dict["CostCtr"]):
        if cost.isdigit() == False or len(cost) < 2:
            print("Invalid cost on row " + str(index + 2) + ": " + cost)
            return False
        
    print("Costs are verified")
    return True

def verifyFile(fileName, fileType):
    fileDict = parseCSV(fileName)
    
    if fileDict == None:
        return False
    
    if (checkLabels(fileDict, fileType) == True 
    and checkDates(fileDict) == True  
    and checkIds(fileDict) == True
    and checkCosts(fileDict) == True):
        return True
    else:
        return False

def verifyFileToStr(fileName, fileType):
    print("Verifying " + fileName + " as filetype " + fileType)
    if verifyFile(fileName, fileType) == True:
        return fileName + " is valid!"
    else:
        fileDict = parseCSV(fileName)
        msg = fileName + ": "
        if fileDict == None:
            msg += "There are empty cells. \n"
            return msg
        if checkLabels(fileDict, fileType) == False:
            msg += "The labels are incorrect. \n"
        if checkDates(fileDict) == False:
            msg += "There are improperly formatted dates."
        if checkIds(fileDict) == False:
            msg += "There are invalid CoIDs."
        if checkCosts(fileDict) == False:
            msg += "There are invalid costs"
        return msg
        

