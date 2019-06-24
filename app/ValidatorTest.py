import pandas as pd
import numpy as np
import datetime
import io
import json

class Validator:
    INVENTORY_LABELS = ["CoID", "Date", "CostCtr", "SHRINKAGE_QTY", "SHRINKAGE_AMT", "BREAKAGE_QTY", "BREAKAGE_AMT", "OVERAGE_QTY", "OVERAGE_AMT"]
    SALES_LABELS = ["CoID", "Date", "CostCtr", "Ces", "Stops", "GP Dollars"]
    PAYROLL_LABELS = ["CoID", "Date", "CostCtr", "ProdHrs", "OTHrs", "ProdDollars", "Headcount"]
    STATIC_PERCENTAGES_LABELS = ["CoID", "Date", "CostCtr", "SBT", "RET", "UNS", "SPE"]
    SETTINGS_FILE = "app/formatSettings.json"
    
    def __init__(self, fileName, fileType):
        self.fileName = fileName
        self.fileType = fileType
        self.settings = dict()
        self.message = ""

    def parseJSON(self):
         with open(self.SETTINGS_FILE) as json_file:  
            self.settings = json.load(json_file)

    def parseCSV(self):
        df = pd.read_csv(self.fileName, dtype='str') #we want strings because some are not ints
        df.columns = df.columns.str.strip()
        if df.isnull().values.any():  #if there are empty cells it will not work
            df1 = df[df.isna().any(axis=1)].index
            self.message += "There are empty cells on row(s): "
            for i in df1:
                self.message += str(i + 2) + " "
            return None
        dict = df.to_dict(orient='list')
        return dict
    
    def checkLabels(self, dict):    
        for validType in self.settings.keys():
            print(validType)
            if self.fileType.lower() == validType.lower():
                return list(dict.keys()) == list(self.settings[validType].keys())
        
        return False

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
                self.message += "Invalid date on row " + str(index + 2) + ": " + date + "<br>"
                return False
        
        print("Dates are verified")
        return True

    #checks if the input has any numbers
    def hasNumber(self, inputString):
        return any(char.isdigit() for char in inputString)

    def is_percentage(self,n):
        if '%' in n:
            return True
        return False

    def checkIds(self, dict):
        print("Checking ids")
        for index, company in enumerate(dict["CoID"]):
            if self.hasNumber(company) or len(company) < 3:
                self.message += "Invalid company id on row " + str(index + 2) + ": " + company + "<br>"
                return False
        
        print("IDs are verified.")
        return True

    #checks that the input can be converted to float (all numbers)
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_percentage(self,n):
        if '%' in n:
            return True
        return False

    def is_string(self,i):
        try:
            int(i)
            return False
        except ValueError:
            return True
            
    def checkColumnIsPosorNeg(self,dict, colIndex, positiveOrNegative):
        for positiveOrNegative in enumerate(dict[list(dict)[colIndex]]):
            if positiveOrNegative < 0:
                for i in enumerate(dict[list(dict)[colIndex]]):
                    if i > 0:
                        return False
                    return True
            if positiveOrNegative > 0:
                for j in enumerate(dict[list(dict)[colIndex]]):
                    if j < 0:
                        return False
                    return True
    
    def checkColIsString(self, dict, )
                
    def checkCosts(self, dict):
        print("Checking costs")
        for index, raw_cost in enumerate(dict["CostCtr"]):
            cost = raw_cost.replace(',','')
            if self.is_number(cost) == False or len(cost) < 2:
                self.message += "Invalid cost on row " + str(index + 2) + ": " + cost + "<br>"
                return False
            
        print("Costs are verified")
        return True

    def checkShrinkageQty(self, dict):
        print("Checking Shrinkage quantities")
        for index, raw_qty in enumerate(dict["SHRINKAGE_QTY"]):
            qty = raw_qty.replace(',','')
            if qty.isdigit() == False or qty > 0:
                self.message += "Invalid shrinkage quantity on row" + str(index + 2) + ": " + qty + "<br>"
                return False

        print("Shrinkage quantities are verified")
        return True

    def checkShrinkageAmt(self, dict):
        print("Checking Shrinkage amounts")
        for index, raw_amt in enumerate(dict["SHRINKAGE_AMT"]):
            amt = raw_amt.replace(',','')
            if self.is_number(amt) == False or amt > 0:
                self.message += "Invalid shrinkage amount on row" + str(index + 2) + ": " + amt + "<br>"
                return False

        print("Shrinkage amounts are verified")
        return True

    def checkBreakageQty(self, dict):
        print("Checking Breakage quantities")
        for index, raw_qty in enumerate(dict["BREAKAGE_QTY"]):
            qty = raw_qty.replace(',','')
            if qty.isdigit() == False or qty > 0:
                self.message += "Invalid breakage quantity on row" + str(index + 2) + ": " + qty + "<br>"
                return False

        print("Breakage quantities are verified")
        return True

    def checkBreakageAmt(self, dict):
        print("Checking Breakage amounts")
        for index, raw_amt in enumerate(dict["BREAKAGE_AMT"]):
            amt = raw_amt.replace(',','')
            if self.is_number(amt) == False or amt > 0:
                self.message += "Invalid breakage amount on row" + str(index + 2) + ": " + amt + "<br>"
                return False

        print("Breakage amounts are verified")
        return True

    def checkOverageQty(self, dict):
        print("Checking Overage quantities")
        for index, raw_qty in enumerate(dict["OVERAGE_QTY"]):
            qty = raw_qty.replace(',','')
            if qty.isdigit() == False or qty > 0:
                self.message += "Invalid overage quantity on row" + str(index + 2) + ": " + qty + "<br>"
                return False

        print("Overage quantities are verified")
        return True

    def checkOverageAmt(self, dict):
        print("Checking Overage amounts")
        for index, raw_amt in enumerate(dict["OVERAGE_AMT"]):
            amt = raw_amt.replace(',','')
            if self.is_number(amt) == False or amt > 0:
                self.message += "Invalid overage amount on row" + str(index + 2) + ": " + amt + "<br>"
                return False

        print("Overage amounts are verified")
        return True

    def checkProdHrs(self, dict):
        print("Checking Prod hours")
        for index, raw_hrs in enumerate(dict["ProdHrs"]):
            hrs = raw_hrs.replace(',','')
            if self.is_number(hrs) == False or float(hrs) < 0:
                self.message += "Invalid prod hours on row" + str(index + 2) + ": " + hrs + "<br>"
                return False

        print("Prod hours are verified")
        return True

    def checkOTHrs(self, dict):
        print("Checking OT hours")
        for index, raw_hrs in enumerate(dict["OTHrs"]):
            hrs = raw_hrs.replace(',','')
            if self.is_number(hrs) == False or float(hrs) < 0:
                self.message += "Invalid OT hours on row" + str(index + 2) + ": " + hrs + "<br>"
                return False

        print("OT hours are verified")
        return True

    def checkProdDollars(self, dict):
        print("Checking Prod dollars")
        for index, raw_dollars in enumerate(dict["ProdDollars"]):
            dollars = raw_dollars.replace(',','')
            if self.is_number(dollars) == False or float(dollars) < 0:
                self.message += "Invalid Prod dollars on row" + str(index + 2) + ": " + dollars + "<br>"
                return False

        print("Prod dollars are verified")
        return True

    def checkHeadcount(self, dict):
        print("Checking Headcount")
        for index, raw_count in enumerate(dict["Headcount"]):
            count = raw_count.replace(',','')
            if self.is_number(count) == False or float(count) < 0:
                self.message += "Invalid Headcount on row" + str(index + 2) + ": " + count + "<br>"
                return False

        print("Headcounts are verified")
        return True
    
    def checkCes(self,dict):
        print("Checking Ces")
        for index, raw_ces in enumerate(dict["Ces"]):
            ces = raw_ces.replace(',','')
            if self.is_number(ces) == False or float(ces) < 0:
                self.message += "Invalid Ces on row" + str(index + 2) + ": " + ces + "<br>"
                return False

        print("Ces are verified")
        return True

    def checkStops(self, dict):
        print("Checking Stops")
        for index, raw_stop in enumerate(dict["Stops"]):
            stop = raw_stop.replace(',','')
            if stop.isdigit() == False or float(stop) < 0:
                self.message += "Invalid Stops on row" + str(index + 2) + ": " + stop + "<br>"
                return False

        print("Stops are verified")
        return True

    def checkGPDollars(self,dict):
        print("Checking GP Dollars")
        for index, raw_dollars in enumerate(dict["GP Dollars"]):
            dollars = raw_dollars.replace(',','')
            if self.is_number(dollars) == False or float(dollars) < 0:
                self.message += "Invalid GP Dollars on row" + str(index + 2) + ": " + dollars + "<br>"
                return False

        print("GP Dollars are verified")
        return True    

    def checkSBT(self,dict):
        print("Checking SBT")
        for index, raw_sbt in enumerate(dict["SBT"]):
            sbt = raw_sbt.replace(',','')
            if sbt[-1] != "%" and self.is_number(sbt[:-1]) == False: 
                self.message += "Invalid SBT on row" + str(index + 2) + ": " + sbt + "<br>"
                return False

        print("SBT are verified")
        return True  

    def checkRET(self,dict):
        print("Checking RET")
        for index, raw_ret in enumerate(dict["RET"]):
            ret = raw_ret.replace(',','')
            if ret[-1] != "%" and self.is_number(ret[:-1]) == False: 
                self.message += "Invalid RET on row" + str(index + 2) + ": " + ret + "<br>"
                return False

        print("RET are verified")
        return True

    def checkUNS(self,dict):
        print("Checking UNS")
        for index, raw_uns in enumerate(dict["UNS"]):
            uns = raw_uns.replace(',','')
            if uns[-1] != "%" and self.is_number(uns[:-1]) == False: 
                self.message += "Invalid UNS on row" + str(index + 2) + ": " + uns + "<br>"
                return False

        print("UNS are verified")
        return True
    
    def checkSPE(self,dict):
        print("Checking SPE")
        for index, raw_spe in enumerate(dict["SPE"]):
            spe = raw_spe.replace(',','')
            if spe[-1] != "%" and self.is_number(spe[:-1]) == False: 
                self.message += "Invalid SPE on row" + str(index + 2) + ": " + spe + "<br>"
                return False

        print("SPE are verified")
        return True

    def verifyFile(self):
        

    def verifyFileToStr(self):
        print("Verifying " + self.fileName + " as filetype " + self.fileType)
        if self.verifyFile() == True:
            return self.fileName + " is valid! Uploaded to /VERIFIED_FILES"
        else:
            return self.fileName + ": <br>" + self.message
        

