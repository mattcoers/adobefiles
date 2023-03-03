#To install Requirements, use: pip3 install -r requirements.txt

import json
import time
import jwt
import datetime
import os
from datetime import datetime, timedelta, timezone, date
import requests
import csv
import sys
import cjapy as cja

import pandas as pd
starttime = time.time()

def PullCRMIDsByDay(day):

    cja.importConfigFile('/Users/coers/datascience/democonfig.json')
    myRequest = cja.RequestCreator()
    
    ## Instantiating the CJA class
    cjaObj  = cja.CJA()

    ## Set the Filter to use a date range
    filterJSON = day ## Format: "2020-12-01T00:00:00.000/2020-12-1T23:59:59.000"

    ## Create Request Dict
    myRequest.setDimension('variables/6054ea5b6701fe194a7fd0c9._usaam.identification.CRMID_1_1')
    myRequest.addMetric('metrics/_usaam.orderDetails.orderFlag')
    myRequest.setDataViewId('dv_60be123172cb1a0859b26ca4')
    myRequest.addGlobalFilter(filterJSON)
    requestDef = myRequest.to_dict()

    ## Return Report Object
    myReport = cjaObj.getReport(requestDef)
    
    ## Convert Report to Data Frame
    reportDataframe = myReport.dataframe
    
    return reportDataframe

#dfCRMIDs = PullCRMIDsByDay("2020-12-01T00:00:00.000/2020-12-1T23:59:59.000")


#Pull CRMIDs and ProductSKU Purchases by Date
for iter in range(1,32):
    dfOutput = pd.DataFrame(columns = ['Date','CRMID','ProductSKU'])
    dt_start = datetime(2020, 12, iter, 0, 0, 0)
    dt_end = datetime(2020, 12, iter, 23, 59, 59)

    print('Input Datetime:', dt_end)

    # convert datetime to ISO date
    iso_date_start = dt_start.isoformat()
    iso_date_end = dt_end.isoformat()
    print('ISO Date Start:', iso_date_start)
    print('ISO Date End:', iso_date_end)

    daterange = iso_date_start + '/' + iso_date_end
    dfCRMIDs = PullCRMIDsByDay(daterange)

    for index, CRMIDrow in dfCRMIDs.iterrows():
        print("CRMIDrow: ", index, ", of ", len(dfCRMIDs))
        
        CRMID = CRMIDrow['variables/6054ea5b6701fe194a7fd0c9._usaam.identification.CRMID_1_1']
        print('crmid: ', CRMID)

        cja.importConfigFile('/Users/coers/datascience/democonfig.json')
        myRequest = cja.RequestCreator()
        #print("myRequest: ", myRequest)

        ## Instantiating the CJA class
        cjaObj  = cja.CJA()

        ## Set the Filter to use a date range
        filterJSON = daterange 

        #myRequest.setDimension('variables/_usaam.productDetails.productSKU')
        myRequest.setDimension('variables/_usaam.productDetails.productSKU')
        myRequest.addMetric('metrics/_usaam.orderDetails.orderFlag')
        
        myRequest.setDataViewId('dv_60be123172cb1a0859b26ca4')
        myRequest.addGlobalFilter(filterJSON)
        CRMIDFilter = 'variables/6054ea5b6701fe194a7fd0c9._usaam.identification.CRMID_1_1:::' + CRMID
        myRequest.addGlobalFilter(CRMIDFilter)
        
        requestDef = myRequest.to_dict()
        myReport = cjaObj.getReport(requestDef)
        #print ("Project: ", myReport)

        reportDataframe = myReport.dataframe
        #print("dataframe: ", reportDataframe)

        for SKUindex, SKUrow in reportDataframe.iterrows(): 
            prodSKU = SKUrow['variables/_usaam.productDetails.productSKU']
            dfOutput.loc[len(dfOutput.index)] = [dt_start, CRMID, prodSKU] 


    #print ("report: ", json.dumps(myInstance, indent=4))
    print('Processing Complete')
    print("dfOutput: ", dfOutput)
    dfOutput.to_csv('/Users/coers/datascience/dfOutput.csv', mode='a', encoding='utf-8', index=False, header=False)
    print('dfOutput File Updated')
    print('sleeping...')
    time.sleep(300)




endtime = time.time()
runtime = endtime - starttime
print('Runtime: ', runtime, ' seconds. ')

