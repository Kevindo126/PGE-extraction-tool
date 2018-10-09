import time
import os
import subprocess
import PyPDF2
import csv
from math import ceil
from tqdm import tqdm
#need to install: sudo pip3 install tqdm
#
#Execute of code:
#python3 oneTest.py
#
#Walkthrough of code:
#First, the program asks for the pdf file of the PGE bill. The program will determine how many pages the PDF has and 
#decides whether to split it into multiple pdfs for faster performance or keep as one pdf.
#Then the program will ask user if they are readt to convert pdf to tiff. Program accepts 'y' for yes and 'n' for no; otherwise 
#the program will quit.
#Once the program converts pdf to tiff, it will ask user if they are ready to convert tiff to a text file using Tesseract.
#This is also a yes or no question.
#Once that is done, the program will create a csv file to capture specific fields from text file.
#The program will take the text files, go through each page from the file and extract to csv file.
#It will repeat this step until all text files are appended into the csv file.



# Boolean values
statementWithFixedUsage = False
statementWithMeterNumber = False
summaryPage = False
meterSummary = False
page1 = True
page2 = False
page3 = False
afterPage3 = False
split = False
convert = False
tesseract  = False
tesseractDone = False
csvStart = False
csvDone = False

# variable declaration
acctNum = ""
fixedUsage = ""
fCount = 0
fixedUsageCheck = []
meterNumber = ""
meterNumCheck = []
locationCheck = []
locationCount = 0
meterCount = 0
serviceAgreementID = ""
fromDate = ""
toDate = ""
serviceLocation = ""
statementDate = ""
totalUsage = ""
usageCheck = []
totalCharge = ""
count = 0
lineCount = 0
esCount = 0
fields = []
x = 0
start = 1
end = 0
dotCount = 0
pdfStartMod = 1
pdfEndMod = 0
outputPDF = []
outputTiff = []
outputFile = []
acctCheck = []
meterCheck = []
serviceIDCheck = []
serviceLocationCheck = []
fixedCheck = []
fromDateCheck = []
toDateCheck = []
statementDateCheck = []
totalUsageCheck = []
totalChargeCheck = []

#Functions
def cleanUp(numOfSplit,numOfPages, pdfMod, folderName, outputPDF, outputTiff, outputFile, tesseract):
    print ("Cleaning up...")

    for k in tqdm(range(0, numOfSplit)):
        #Delete PDF once done converting it
        try:
            if convert == True and tesseract == False:
                remove = outputPDF[k]
                os.remove(remove)
            #Delete tiff
            if tesseract:
                remove = outputTiff[k]
                os.remove(remove)
            #Delete txt documents
            if csvDone:
                remove = outputFile[k] + ".txt"
                os.remove(remove)
        except:
            break
    return
def clearCheckList():
    acctCheck.clear()
    meterCheck.clear()
    serviceIDCheck.clear()
    serviceLocationCheck.clear()
    fixedCheck.clear()
    fromDateCheck.clear()
    toDateCheck.clear()
    statementDateCheck.clear()
    totalUsageCheck.clear()
    usageCheck.clear()
    totalChargeCheck.clear()
    fields.clear()
    return
def resetFields():
    acctNum = ""
    fixedUsage = ""
    meterNumber = ""
    meterCount = 0
    serviceAgreementID = ""
    fromDate = ""
    toDate = ""
    serviceLocation = ""
    statementDate = ""
    totalUsage = ""
    totalCharge = ""
    return
def accountArray(acctCheck):
    aCount = 0
    acctCheckLen = 11
    for a in range(0, len(acctCheck)):
        if acctCheck[a] != "NA":
            if acctCheckLen == 11:
                acctTemp = acctCheck[a]
                acctCheck.clear()
                acctCheck.append(acctTemp)
                aCount = 0
                return acctCheck[0]
        if acctCheck[a] == "NA" or acctCheck[a] == " ":
            aCount += 1
            if aCount == (len(acctCheck)):
                acctCheck.clear()
                acctCheck.append("NA")
                aCount = 0
                return acctCheck[0]
def meterArray(meterCheck):
    mCount = 0
    for b in range(0, len(meterCheck)):
            if meterCheck[b] != "NA":
                meterTemp = meterCheck[b]
                meterCheck.clear()
                meterCheck.append(meterTemp) #fixed append(meterTemp[0]) to meterTemp
                mCount = 0
                return meterCheck[0]
            elif meterCheck[b] == "NA":
                mCount += 1
                if mCount == (len(meterCheck)):
                    meterCheck.clear()
                    meterCheck.append("NA")
                    mCount = 0
                    return meterCheck[0]
def fixedArray(fixedCheck):
    fixedCount = 0
    for c in range(0, len(fixedCheck)):
            if fixedCheck[c] != "NA":
                fixedTemp = fixedCheck[c]
                fixedCheck.clear()
                fixedCheck.append(fixedTemp) #fixed append(fixedTemp[0]) to fixedTemp
                fixedCount = 0
                return fixedCheck[0]
            elif fixedCheck[c] == "NA":
                fixedCount += 1
                if fixedCount == (len(fixedCheck)):
                    fixedCheck.clear()
                    fixedCheck.append("NA")
                    fixedCount = 0
                    return fixedCheck[0]
def statementDateArray(statementDateCheck):
    statementCount = 0
    for d in range(0, len(statementDateCheck)):
            if statementDateCheck[d] != "NA":
                statmentTemp = statementDateCheck[d]
                statementDateCheck.clear()
                statementDateCheck.append(statmentTemp)
                statementCount = 0
                return statementDateCheck[0]
            elif statementDateCheck[d] == "NA":
                statementCount += 1
                if statementCount == (len(statementDateCheck)):
                    statementDateCheck.clear()
                    statementDateCheck.append("NA")
                    statementCount = 0
                    return statementDateCheck[0]
def totalUsageArray(totalUsageCheck):
    usageCount = 0
    for e in range(0, len(totalUsageCheck)):
        if totalUsageCheck[e] != "NA" and totalUsageCheck[e] != "":
            usageTemp = totalUsageCheck[e]
            totalUsageCheck.clear()
            totalUsageCheck.append(usageTemp)
            usageCount = 0
            return totalUsageCheck[0]
        elif totalUsageCheck[e] == "NA":
            usageCount += 1
            if usageCount == (len(totalUsageCheck)):
                totalUsageCheck.clear()
                totalUsageCheck.append("NA")
                usageCount = 0
                return totalUsageCheck[0]
def usageCheckArray(usageCheck):
    useCheckCount = 0
    for g in range (0, len(usageCheck)):
        if usageCheck[g] != "NA":
            useCheckTemp = usageCheck[g]
            usageCheck.clear()
            usageCheck.append(useCheckTemp)
            useCheckCount = 0
            return usageCheck[0]
        elif usageCheck[g] == "NA":
            useCheckCount += 1
            if useCheckCount == len(usageCheck):
                usageCheck.clear()
                usageCheck.append("NA")
                useCheckCount = 0
                return usageCheck[0]
def finalizeTotalUsage(usageCheck, totalUsageCheck):
    try:
        if totalUsageCheck[0] != usageCheck[0] and len(usageCheck) > 0:
            if totalUsageCheck[0] == "NA" or totalUsageCheck[0] == "" and usageCheck[0] != "NA":
                totalUsageCheck.clear()
                totalUse = usageCheck[0]
                totalUsageCheck.append(totalUse)
                return totalUsageCheck
            elif usageCheck[0] != "NA" and usageCheck[0] != "" and totalUsageCheck[0] != "NA":
                totalUsageCheck.clear()
                totalUse = usageCheck[0]
                totalUsageCheck.append(totalUse)
                return totalUsageCheck
            elif usageCheck[0] == "NA" or usageCheck[0] == "" or usageCheck[0] is None and totalUsageCheck[0] != "NA":
                return totalUsageCheck
    except:
        return totalUsageCheck
def locationArray(serviceLocationCheck):
    lCount = 0
    for f in range(0, len(serviceLocationCheck)):
        if serviceLocationCheck[f] != "NA":
            locaTemp = serviceLocationCheck[f]
            serviceLocationCheck.clear()
            serviceLocationCheck.append(locaTemp)
            lCount = 0
            return serviceLocationCheck[0]
        elif serviceLocationCheck[f] == "NA":
            lCount += 1
            if lCount == (len(serviceLocationCheck)):
                serviceLocationCheck.clear()
                serviceLocationCheck.append("NA")
                lCount = 0
                return serviceLocationCheck[0]
def combineFields(acctCheck, meterCheck, serviceIDCheck, serviceLocationCheck, fixedCheck, fromDateCheck, toDateCheck, statementDateCheck, totalUsageCheck, totalChargeCheck, fields):
    fields.extend(acctCheck)
    fields.extend(meterCheck)
    fields.extend(serviceIDCheck)
    fields.extend(serviceLocationCheck)
    fields.extend(fixedCheck)
    fields.extend(fromDateCheck)
    fields.extend(toDateCheck)
    fields.extend(statementDateCheck)
    fields.extend(totalUsageCheck)
    fields.extend(totalChargeCheck)
    return fields

def isDecimal(fixedUsage):
    try:
        float(fixedUsage)
    except ValueError:
        return False
    else:
        return True

print("What is the PDF file name?")
pdf = input()
pdfFileObj = open(pdf, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
numOfPages = pdfReader.numPages
print ("Number of pages in pdf: ", numOfPages)
pdfMod = pdf.replace(".pdf", "")
print (pdfMod)
print ("--------------")
# Splitting up PDF
if numOfPages > 8:
    # Create Folder
    print("There are lots pages in the PDF that needs to be split up, lets create a folder for it and I'll take care of splitting")
    print("Please give a name for this folder:")
    folderName = input()
    print ("--------------")
    split = True
    #Make Folder
    command = 'mkdir /home/kdpc/Desktop/' + folderName
    os.system(command)
    move = "mv " + pdf + " " + folderName
    os.system(move)
    path = "/home/kdpc/Desktop/" + folderName
    os.chdir(path)
    # Split
    numOfSplit = ceil(pdfReader.numPages/8)
    print ("Splitting up PDF...Total number of pdfs: ", numOfSplit)

    for x in tqdm(range(0, numOfSplit)):
        end = start + 7
        if end > numOfPages:
            command = 'pdftk ' + pdf + ' cat ' + str(start) + '-' + str(numOfPages) + ' output ' + pdfMod + "-Page" + str(start) + "-" + str(numOfPages) +".pdf"
            outputPDF.append(pdfMod + "-Page" + str(start) + "-" + str(numOfPages) +".pdf")
            os.system(command)
        else:
            command = 'pdftk ' + pdf + ' cat ' + str(start) + '-' + str(end) + ' output ' + pdfMod + "-Page" + str(start) + "-" + str(end) +".pdf"
            outputPDF.append(pdfMod + "-Page" + str(start) + "-" + str(end) +".pdf")
            os.system(command)
        start = start + 8
    print ("Done splitting...")
else:
    numOfSplit = 1
#convert PDF to tiff
while True:
    print ("Are you ready to convert the pdf file to a tiff?")
    response = input("Enter y- yes | n- no:")
    if response == "" or not response in ['y','n']:
        print("Error, did not recognize your input. Please try again!")
        convert = False
    else:
        break
if response == "y":
    if split:
        try:
            print ("Converting...This may take a while, please wait!")
            for j in tqdm(range(0, numOfSplit)):
                pdfEndMod = pdfStartMod + 7
                if pdfEndMod > numOfPages:
                    command = 'convert -density 300 ' + pdfMod + "-Page" + str(pdfStartMod) + "-" + str(numOfPages) +".pdf"+' -depth 8 ' + pdfMod + "-Page" + str(pdfStartMod) + "-" + str(numOfPages) + ".tiff"
                    outputTiff.append(pdfMod + "-Page" + str(pdfStartMod) + "-" + str(numOfPages) + ".tiff")
                    os.system(command)
                else:
                    command = 'convert -density 300 ' + pdfMod + "-Page" + str(pdfStartMod) + "-" + str(pdfEndMod) +".pdf"+' -depth 8 ' + pdfMod + "-Page" + str(pdfStartMod) + "-" + str(pdfEndMod) + ".tiff"
                    outputTiff.append(pdfMod + "-Page" + str(pdfStartMod) + "-" + str(pdfEndMod) + ".tiff")
                    os.system(command)
                pdfStartMod = pdfStartMod + 8
            print ("Done Converting multiple pdf!")
            convert = True
            #Delete PDF
            cleanUp(numOfSplit,numOfPages, pdfMod, folderName, outputPDF, outputTiff, outputFile, tesseract)
        except:
            print("Something went wrong!!!")
    elif split == False:
        #If pdf did not split or just 1 PDF.
        command = 'convert -density 300 ' + pdf +' -depth 8 ' + pdfMod + '.tiff'
        outputTiff.clear()
        outputTiff.append(pdfMod + '.tiff')
        os.system(command)
        print ("Done Converting 1 pdf!")
        convert = True
elif response == "n":
    print ("Did not convert to tiff")
    convert = False

#tesseract -tiff to txt
if convert:
    while True:
        print ("Do you want tesseract to extract text?")
        answer = input("Enter y- yes | n- no:")
        if answer == "" or not answer in ['y','n']:
            print("Error, did not recognize your input. Please try again!")
            tesseract = False
        else:
            break
    if answer == "y":
        if split:
            for n in range(0, numOfSplit):
                txtfile = outputTiff[n].replace(".tiff", "")
                outputFile.append(txtfile)
                print (outputFile[n])

            print ("Initiating tesseract...")
            for i in range(0, numOfSplit):
                command = "tesseract " + outputTiff[i] + " " + outputFile[i]
                print (command)
                os.system(command)
                print ("Done")
            tesseract = True
            tesseractDone = True
            #Delete tiff and move txt documents to folder
            cleanUp(numOfSplit,numOfPages, pdfMod, folderName, outputPDF, outputTiff, outputFile, tesseract)
            tesseract = False
            convert = False
        else:
            command = "tesseract " + pdfMod + ".tiff " + pdfMod
            print (command)
            os.system(command)
            print("Done")
    elif answer == "n":
        print ("Did not use tesseract")
        tesseract = False
        
# Open the file with read only permit
if tesseractDone:
    for m in range(0, numOfSplit):
        txtdoc = outputFile[m] + ".txt"
        print (txtdoc)
        readTxt = open(txtdoc)
        csvdoc = outputFile[0].split("-Page")
        csvdoc = csvdoc[0] + ".csv"
        
        #This is to start append mode after writing first line
        if csvStart:
            writeTxt = open(csvdoc, "a")

        # This to set/reset lineCount 
        lineCount = 0
        # use readline() to read the first line 
        line = readTxt.readline()

        # write the first line
        if csvStart == False:
            writeTxt = open(csvdoc, "w")
            writeTxt.write("AccountNumber, MeterNumber, ServiceAgreementID, serviceLocation, fixedUsage, FromDate, ToDate, statementDate, TotalUsage, TotalCharge" + "\n")
        csvStart = True
        #Get total # of lines in file
        lines = len(open(txtdoc).readlines())

        for x in range(0, lines): #changed from while lines:
            lineCount += 1
            # May need to do some changes for page.
            if "Electric Monthly Billing History" in line:
                page1 = True
            if "Page 1 of" in line or "Important Phone Numbers" in line:
                page2 = True
                page1 = False
                page3 = False
            if "Page 2 of" in line:
                page1 = False
                page2 = False
                page3 = True
                clearCheckList()
                resetFields()
            # summary page recognition
            if "Summary of your energy related services" in line and page3:
                summaryPage = True
            else:
                summaryPage = False
            if "Page 3 of" in line:
                page1 = False
                page2 = False
                page3 = False
                afterPage3 = True
                summaryPage = False

            # Account number
            if "Account No" in line and summaryPage == False:
                try:
                    acctSplit = line.partition("-")
                    acctSec = acctSplit[2].rstrip('"\n')
                    if acctSec[0].isnumeric():
                        acctSep = acctSplit[0].split(" ")
                        acctlen = len(acctSep)
                        if acctSep[acctlen -1].isnumeric():
                            acctFirst = acctSep[acctlen -1]
                        elif acctSep[acctlen - 2].isnumeric():
                            acctFirst = acctSep[acctlen - 2]
                        acctNum = acctFirst + acctSec[0]
                        acctCheck.append(acctNum)
                    elif acctSec is None:
                        acctNum = "NA"
                        acctCheck.append(acctNum)
                    else:
                        acctNum = "NA"
                        acctCheck.append(acctNum)
                except:
                    acctNum = "NA"
                    acctCheck.append(acctNum)

            # For purpose of double checking meter #
            if "Electric Charges" in line[0:16] and summaryPage:
                ECSplit = line.split("Electric Charges ")
                EC = ECSplit[1].rstrip("\n")
                meterNumCheck = meterNumCheck + [EC]
                meterSummary = True
            #Actual meter number
            if "Meter #" in line and summaryPage == False:
                statementWithMeterNumber = True
                statementWithFixedUsage = False
                try:
                    meterCount += 1
                    meterSplit = line.partition("#")
                    meterNumSplit = meterSplit[2].lstrip(" ")
                    meterNumber = meterNumSplit.rstrip(" _\n")
                    meterNumber = meterNumber[0:10]
                    if not meterNumber.isnumeric() and meterSummary == True:
                        meterNumber = meterNumCheck[meterCount -1]
                    meterCheck.append(meterNumber)
                except:
                    pass
                    meterNumber = "NA"
                    meterCheck.append(meterNumber)
            else:
                meterNumber = "NA"
                meterCheck.append(meterNumber)
            #Service Agreement ID
            if "Service Agreement ID" in line and summaryPage == False: #delete page3 = False
                IDSplit = line.partition("ID: ")
                IDNum = IDSplit[2].lstrip(" ")
                serviceID = IDNum.partition(" ")
                serviceAgreementID = serviceID[0]
                if serviceAgreementID.isnumeric():
                    serviceIDCheck.append(serviceAgreementID)

            #For purpose of double checking the correct service location
            if "Service For" in line and summaryPage == True:
                locationSplit = line.split("Service For:")
                LC = locationSplit[1].rstrip("\n")
                LC = LC.lstrip()
                locationCheck = locationCheck + [LC]
            #Actual service location
            if "Service For" in line and summaryPage == False:
                try:
                    locationSplit = line.partition("For")
                    serviceLocation = locationSplit[2].lstrip(",;: ")
                    serviceLocation = serviceLocation.rstrip("Serial B \n")
                    if "Service" in serviceLocation:
                        serviceLocation = serviceLocation.partition("Service")
                        if serviceLocation[0] == '':
                            serviceLocation = "NA"
                            serviceLocationCheck.append(serviceLocation)
                        else:
                            serviceLocation = serviceLocation[0]
                            serviceLocationCheck.append(serviceLocation)
                    elif "Prior" in serviceLocation:
                        serviceLocation = serviceLocation.partition("Prior")
                        serviceLocation = serviceLocation[0].rstrip(" ")
                        serviceLocationCheck.append(serviceLocation)
                    else:
                        serviceLocationCheck.append(serviceLocation)

                    # double checking feature
                    locationCount += 1
                    if serviceLocation != locationCheck[locationCount - 1]:
                        serviceLocation = locationCheck[locationCount-1]
                    serviceLocationCheck.append(serviceLocation)
                except:
                    if "," in serviceLocation:
                        commaSplit = serviceLocation.replace(',','')
                        serviceLocation = commaSplit.rstrip("\n")
                        serviceLocationCheck.append(serviceLocation)
                    else:
                        serviceStrip = serviceLocation.rstrip("\n")
                        serviceLocation = serviceStrip
                        serviceLocationCheck.append(serviceLocation)
            
            # From Date and To Date
            if "billing days)" in line:
                dateSplit = line.split("-")
                fromDate = dateSplit[0].rstrip(" ")
                toDate = dateSplit[1].rsplit(None)
                toDate = toDate[0]
                if len(fromDate) > 10:
                    fromDate = fromDate.rpartition(" ")
                    fromDate = fromDate[2]
                fromDateCheck.append(fromDate)
                toDateCheck.append(toDate)

            #Statement Date
            if "Statement Date" in line and summaryPage == False:
                dateSplit = line.partition("Statement Date:")
                try:
                    if dateSplit[2] == "\n" or dateSplit[1] == "\t":
                        statementDate = "NA"
                        statementDateCheck.append(statementDate)
                    elif dateSplit[2] == '':
                        statementDate = "NA"
                        statementDateCheck.append(statementDate)
                    else:
                        statementDate = dateSplit[2].rstrip("\n\t")
                        statementDate = statementDate.lstrip(" \t\n")
                        if len(statementDate) == 10:
                            statementDateCheck.append(statementDate)
                except:
                    statementDate = "NA"
                    statememeterCountmeterCountntDateCheck.append(statementDate)
            else:
                statementDate = "NA"
                statementDateCheck.append(statementDate)

            # For purpose of double checking totalUsage 
            if "Electric Usage This Period" in line:
                energySplit = line.partition("Period:")
                UC = energySplit[2].partition("kWh")
                UC = UC[0].lstrip(" \t")
                UC = UC.rstrip(" ")
                UC = UC.replace(" ", "")
                if UC[0].isdigit():
                    if "," in UC:
                        UC = UC.replace(",", ".")
                        dotUCCount = UC.count('.')
                        if dotUCCount >= 2:
                            UC = UC.replace(".", "", 1)
                        usageCheck = usageCheck + [UC]
                    else:
                        usageCheck = usageCheck + [UC]
                else:
                    usageCheck.append("NA")
                
            # Actual totalUsage
            if "Total Usage" in line:
                try:
                    usageSplit = line.partition("Total Usage")
                    totalUsage = usageSplit[2].rstrip("\n kWh")
                    totalUsage = totalUsage.lstrip(" ")
                    if "," in totalUsage:
                        totalUsage = totalUsage.replace(",", ".")
                        dotTUCount = totalUsage.count('.')
                        if dotTUCount >= 2:
                            totalUsage = totalUsage.replace('.', '', 1)
                    totalUsageCheck.append(totalUsage)
                except IndexError:
                    pass
                    totalUsage = "NA"
                    totalUsageCheck.append(totalUsage)
            else:
                totalUsage = "NA"
                totalUsageCheck.append(totalUsage)

            # Total Electric Charges
            if "Total Electric Charges" in line and summaryPage == False:
                totalCharge = line.lstrip("Total Electric Charges $")
                totalCharge = totalCharge.rstrip('\n')
                totalCharge = totalCharge.replace(' |', '')
                totalCharge = totalCharge.lstrip('\t')
                if "," in totalCharge:
                    chargeSplit = totalCharge.split(',')
                    totalCharge = chargeSplit[0] + chargeSplit[1]
                    totalCharge = totalCharge.replace('\t', '') 
                elif " " in totalCharge or len(totalCharge) == 0:
                    totalCharge = "NA"
                totalChargeCheck.append(totalCharge)

            # Total PG&E Electric Delivery Charges
            if "Total PG&E Electric Delivery Charges" in line and afterPage3:
                totalCharge = line.lstrip("Total PG&E Electric Delivery Charges $")
                totalCharge = totalCharge.rstrip()
                if "," in totalCharge:
                    chargeSplit = totalCharge.split(',')
                    totalCharge = chargeSplit[0] + chargeSplit[1]
                    totalCharge = totalCharge.replace('\t', '') 
                elif " " in totalCharge or len(totalCharge) == 0:
                    totalCharge = "NA"
                totalChargeCheck.append(totalCharge)

            # for purpose of double checking fixed usage
            if "Energy Charges" in line and "kWh" in line and statementWithFixedUsage:
                energyCharge = line.split('kWh')
                energyCheck = energyCharge[0].rpartition(' ')
                energyCheck = energyCheck[0].lstrip('Energy Charges\t')
                if isDecimal(energyCheck) is True:
                    if energyCheck != fixedUsage:
                        fixedUsage = energyCheck
                        fixedCheck.append(fixedUsage) 
                else:
                    energyCheck = "NA"
                    fixedCheck.append(fixedUsage)
                   
            #actual fixed usage values
            if "Fixed Usage" in line and not "Service-Fixed Usage" in line:
                
                statementWithFixedUsage = True
                statementWithMeterNumber = False
                meterCheck.clear()
                meterCheck.append("NA")
                fCount += 1
                fixedSplit = line.split("Fixed Usage ")
                fixedUsage = fixedSplit[1].lstrip('\t')
                fixedUsage = fixedUsage[0:8]
                fixedUsage = fixedUsage.replace(',', '.')
                if "." in fixedUsage:
                    dotCount = fixedUsage.count('.', 0, len(fixedUsage))
                    if dotCount >= 2:
                        fixedUsage = fixedUsage.replace('.', '', 1)
                if not fixedUsage.isalpha():
                    fixedCheck.append(fixedUsage)
                    # totalUsageCheck.append(fixedUsage)
                    fCount = 0
                else:
                    fixedUsage = "NA"
                    fixedCheck.append(fixedUsage)

            #getting ready to print
            #If everything works then get rid of print functions get rid of count 
            if "Details of Electric Charges" in line and afterPage3 and summaryPage == False and page1 == False and page2 == False: 
                esCount += 1
                if esCount == 1:
                    continue
                else:
                    count += 1
                    print (count)

                    accountArray(acctCheck)
                    print (acctCheck)

                    meterArray(meterCheck)
                    print (meterCheck)

                    print (serviceIDCheck) 

                    locationArray(serviceLocationCheck)
                    print (serviceLocationCheck)

                    fixedArray(fixedCheck)
                    print (fixedCheck)

                    print (fromDateCheck)
                    print (toDateCheck)

                    statementDateArray(statementDateCheck)  
                    print (statementDateCheck)

                    totalUsageArray(totalUsageCheck)
                    usageCheckArray(usageCheck)
                    finalizeTotalUsage(usageCheck, totalUsageCheck)
                    print (totalUsageCheck)
                    
                    print (totalChargeCheck)
                    print ("----------------")
                    combineFields(acctCheck, meterCheck, serviceIDCheck, serviceLocationCheck, fixedCheck, fromDateCheck, toDateCheck, statementDateCheck, totalUsageCheck, totalChargeCheck, fields)
                    if len(fields) == 10:
                        print (fields)

                        # if statement version has meter number
                        if statementWithMeterNumber:          
                            for i in range(0 , len(fields)):
                                if i == len(fields) - 1:
                                    writeTxt.write(fields[i] + "\n")
                                    break
                                else:
                                    writeTxt.write(fields[i] + ",")
                            print ("=======*========")
                            fields.clear()
                            resetFields()
                        # if statement version has fixed usage            
                        if statementWithFixedUsage:
                            for h in range(0 , len(fields)):
                                if h == len(fields) - 1:
                                    writeTxt.write(fields[h] + "\n")
                                    break
                                else:
                                    writeTxt.write(fields[h] + ",")
                            print ("================")
                            fields.clear()
                            resetFields()
                clearCheckList()
            # For printing the last part
            if lineCount == lines:
                count += 1
                print (count)

                accountArray(acctCheck)
                print (acctCheck)

                meterArray(meterCheck)
                print (meterCheck)

                print (serviceIDCheck)

                locationArray(serviceLocationCheck)
                print (serviceLocationCheck)

                fixedArray(fixedCheck)
                print (fixedCheck)

                print (fromDateCheck)
                print (toDateCheck)

                statementDateArray(statementDateCheck)  
                print (statementDateCheck)

                totalUsageArray(totalUsageCheck)
                usageCheckArray(usageCheck)
                finalizeTotalUsage(usageCheck, totalUsageCheck)
                print (totalUsageCheck)
                
                print (totalChargeCheck)
                print ("----------------")
                combineFields(acctCheck, meterCheck, serviceIDCheck, serviceLocationCheck, fixedCheck, fromDateCheck, toDateCheck, statementDateCheck, totalUsageCheck, totalChargeCheck, fields)
                if len(fields) == 10:
                    print (fields)

                    # if statement version has meter number
                    if statementWithMeterNumber:          
                        for i in range(0 , len(fields)):
                            if i == len(fields) - 1:
                                writeTxt.write(fields[i] + "\n")
                                break
                            else:
                                writeTxt.write(fields[i] + ",")
                        print ("=======*========")
                        fields.clear()
                        resetFields()
                    # if statement version has fixed usage            
                    if statementWithFixedUsage:
                        for h in range(0 , len(fields)):
                            if h == len(fields) - 1:
                                writeTxt.write(fields[h] + "\n")
                                break
                            else:
                                writeTxt.write(fields[h] + ",")
                        print ("================")
                        fields.clear()
                        resetFields()
                clearCheckList()
            # use realine() to read next line
            line = readTxt.readline()
        count = 0
            
        csvDone = True
        # Delete txt file
        cleanUp(numOfSplit,numOfPages, pdfMod, folderName, outputPDF, outputTiff, outputFile, tesseract)
        count = 0
        readTxt.close()
        writeTxt.close()
        csvDone = False
else:
    print("Could not process text because tesseract did not extract!")


print("Complete!")
time.sleep(5)
#time in seconds
