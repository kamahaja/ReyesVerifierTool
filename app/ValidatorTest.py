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
    if (fileType.lower() == "inventory"):
        return list(dict.keys()) == INVENTORY_LABELS
    elif (fileType.lower() == "sales"):
        return list(dict.keys()) == SALES_LABELS
    elif (fileType.lower() == "payroll"):
        return list(dict.keys()) == PAYROLL_LABELS
    else:
        return list(dict.keys()) == STATIC_PERCENTAGES_LABELS

def validateDateFormat(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m/%d/%Y')
        return True
    except ValueError:
        return False
        #raise ValueError("Incorrect data format, should be MM-DD-YYYY")

def checkDates(dict):
    for date in dict["Date"]:
        if validateDateFormat(date) == False:
            return False
        
    return True

def hasNumber(inputString):
    return any(char.isdigit() for char in inputString)

def checkIds(dict):
    for index, company in enumerate(dict["CoID"]):
        if hasNumber(company) or len(company) < 3:
            print("Invalid company id on row " + str(index + 2) + ": " + company)
            return False
        
    return True

def checkCosts(dict):
    for index, cost in enumerate(dict["CostCtr"]):
        if cost.isdigit() == False or len(cost) < 2:
            print("Invalid cost on row " + str(index + 2) + ": " + cost)
            return False
        
        
    return True

def verifyFile(fileName, fileType):
    fileDict = parseCSV(fileName)
    
    if fileDict == None:
        return False
    
    if (checkLabels(fileDict, fileType) == True 
    and checkDates(fileDict) == True  
    and checkIds(fileDict) == True):
        return True
    else:
        return False

def verifyFileToStr():
    return "It's passing the information in correctly"

