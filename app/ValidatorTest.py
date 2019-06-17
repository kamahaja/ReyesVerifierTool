import pandas as pd
import numpy as np
import datetime

class Validator:
    INVENTORY_LABELS = ["CoID", "Date", "CostCtr", "SHRINKAGE_QTY", "SHRINKAGE_AMT", "BREAKAGE_QTY", "BREAKAGE_AMT", "OVERAGE_QTY", "OVERAGE_AMT"]
    SALES_LABELS = ["CoID", "Date", "CostCtr", "Ces", "Stops", "GP Dollars"]
    PAYROLL_LABELS = ["CoID", "Date", "CostCtr", "ProdHrs", "OTHrs", "ProdDollars", "Headcount"]
    STATIC_PERCENTAGES_LABELS = ["CoID", "Date", "CostCtr", "SBT", "RET", "UNS", "SPE"]
    
    def __init__(self, fileName, fileType):
        self.fileName = fileName
        self.fileType = fileType
        self.message = ""

    def parseCSV(self):
        df = pd.read_csv(self.fileName, dtype='str') #we want strings because some are not ints
        df.columns = df.columns.str.strip()
        if df.isnull().values.any():  #if there are empty cells it will not work
            self.message += "There are empty cells! \n"
            return None
        dict = df.to_dict(orient='list')
        return dict

    def checkLabels(self, dict):
        areLabelsCorrect = False
        if (self.fileType.lower() == "inventory"):
            areLabelsCorrect = list(dict.keys()) == self.INVENTORY_LABELS
            if areLabelsCorrect == False:
                self.message += "The labels do not match up with inventory labels."
        elif (self.fileType.lower() == "sales"):
            areLabelsCorrect = list(dict.keys()) == self.SALES_LABELS
            if areLabelsCorrect == False:
                self.message += "The labels do not match up with sales labels."
        elif (self.fileType.lower() == "payroll"):
            areLabelsCorrect = list(dict.keys()) == self.PAYROLL_LABELS
            if areLabelsCorrect == False:
                self.message += "The labels do not match up with payroll labels."
        else:
            areLabelsCorrect = list(dict.keys()) == self.STATIC_PERCENTAGES_LABELS
            if areLabelsCorrect == False:
                self.message += "The labels do not match up with static percentages labels."

        print("Labels are verified: " + str(areLabelsCorrect))
        return areLabelsCorrect

    def validateDateFormat(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%m/%d/%Y')
            return True
        except ValueError:
            return False
            #raise ValueError("Incorrect data format, should be MM-DD-YYYY")

    def checkDates(self, dict):
        print("Checking dates")
        for index, date in enumerate(dict["Date"]):
            if self.validateDateFormat(date) == False:
                self.message += "Invalid date on row " + str(index + 2) + ": " + date
                return False
        
        print("Dates are verified")
        return True

    def hasNumber(self, inputString):
        return any(char.isdigit() for char in inputString)

    def checkIds(self, dict):
        print("Checking ids")
        for index, company in enumerate(dict["CoID"]):
            if self.hasNumber(company) or len(company) < 3:
                self.message += "Invalid company id on row " + str(index + 2) + ": " + company
                return False
        
        print("IDs are verified.")
        return True

    def checkCosts(self, dict):
        print("Checking costs")
        for index, cost in enumerate(dict["CostCtr"]):
            if cost.isdigit() == False or len(cost) < 2:
                self.message += "Invalid cost on row " + str(index + 2) + ": " + cost
                return False
            
        print("Costs are verified")
        return True

    def verifyFile(self):
        fileDict = self.parseCSV()
        
        if fileDict == None:
            return False
        
        if (self.checkLabels(fileDict) == True 
        and self.checkDates(fileDict) == True  
        and self.checkIds(fileDict) == True
        and self.checkCosts(fileDict) == True):
            return True
        else:
            return False

    def verifyFileToStr(self):
        print("Verifying " + self.fileName + " as filetype " + self.fileType)
        if self.verifyFile() == True:
            return self.fileName + " is valid!"
        else:
            return self.message
        

