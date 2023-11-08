#Libraries
import requests
import json
import pandas as pd

#Support Functions
from headerSettings import headerSettings
from cjaQuery import cjaQuery

query = cjaQuery()
url = "https://cja.adobe.io/reports"  
headerObject = headerSettings()

response = requests.post(url, headers=headerObject, data=json.dumps(query))

rows = response.json()['rows']

listData = []
for row in rows:
    rowData = {}
    rowData['pageName'] = row['value']
    rowData['visitors'] = row['data'][0]
    listData.append(rowData)

dfData = pd.DataFrame(listData)
print(dfData)