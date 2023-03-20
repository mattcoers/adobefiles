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
#print(dfBasketAssocRules.head())

#Join Data Frame to recommend next product by CRMID
dfPredicted = dfProductPurchases.sort_values(by=['crmid','date'], ascending=False)
dfPredicted.rename(columns={'sku':'lastSKU'}, inplace=True)

dfBasketRulesCP = pd.DataFrame(dfBasketAssocRules, copy=True)
dfBasketRulesCP["antecedents"] = dfBasketRulesCP["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
dfBasketRulesCP["consequents"] = dfBasketRulesCP["consequents"].apply(lambda x: list(x)[0]).astype("unicode")
dfBasketRulesCP.rename(columns={'antecedents':'lastSKU'}, inplace=True)
dfBasketRulesCP.rename(columns={'consequents':'nextSKU'}, inplace=True)

dfPredicted = pd.merge(dfPredicted, dfBasketRulesCP, on='lastSKU', how='inner')
dfPredicted.drop_duplicates('crmid', keep='first', inplace=True)
dfPredicted = dfPredicted.dropna()
dfPredicted.drop(columns=['single_transaction', 'antecedent support','consequent support','leverage','conviction','date'], inplace=True)
dfPredicted.sort_values(["crmid"], axis=0, ascending=False)

dfPredicted.to_csv('/Users/coers/datascience/dfPredicted.csv', encoding='utf-8', index=False, header=True)

print("dfPredicted: ")
print(dfPredicted.head(500))

### PRINT TIME TRACKING ###
endtime = time.time()
runtime = endtime - starttime
print('Runtime: ', runtime, ' seconds. ')
