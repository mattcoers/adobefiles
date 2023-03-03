#To install Requirements, use: pip3 install -r requirements.txt

import time
from datetime import datetime, timedelta, timezone, date
import cjapy as cja
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

### START TIME TRACKING ###

starttime = time.time()

### FUNCTION DEFINITIONS ###
def encodeMap(numPurchased):
    num = 0
    if numPurchased > 0:
        num = 1
    return num

### APPLICATION LOGIC ###

#Read dfOutput.csv file and load it into a Data Frame
dfProductPurchases = pd.read_csv('/Users/coers/datascience/dfOutput.csv')
#print(dfProductPurchases.head())

#Concatenate the Person ID and the Product SKU to create a new column in the Data Frame
dfProductPurchases['single_transaction'] = dfProductPurchases['crmid'].astype(str)+'-' + dfProductPurchases['date'].astype(str)
#print(dfProductPurchases.head())

#Pivot the Data Frame to convert transactions into rows and items into columns
dfTransactionPivot = pd.crosstab(dfProductPurchases['single_transaction'], dfProductPurchases['sku'])
#print(dfTransactionPivot.head())

#Convert number of purchases to 1 or 0
dfEncoded = dfTransactionPivot.applymap(encodeMap)
#print(dfEncoded.head())

#Execute Apriori Algo
dfCommonBaskets = apriori(dfEncoded.astype('bool'), min_support=0.001, use_colnames=True)
dfBasketAssocRules = association_rules(dfCommonBaskets, metric="lift")
dfBasketAssocRules.sort_values(["support","confidence","lift"], axis=0, ascending=False)
print(dfBasketAssocRules.head())

### PRINT TIME TRACKING ###
endtime = time.time()
runtime = endtime - starttime
print('Runtime: ', runtime, ' seconds. ')
