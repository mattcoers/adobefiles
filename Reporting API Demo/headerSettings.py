from accessToken import getToken

def headerSettings():
    accessToken = getToken()
    myHeader = {
        "x-gw-ims-org-id" : "[INSERT IMS ORG ID HERE]",
        "x-api-key" : "[INSERT API KEY (CLIENT ID) HERE]",
        "authorization" : f"Bearer {accessToken}",
        "Content-Type": "application/json"
    }
    return myHeader