##python test file for flask to test locally
import requests as r
import pandas as pd
import json

base_url = 'http://127.0.0.1:5000/' #base url local host

#Get reponse on data from inputed excel file
test = pd.read_excel("toy_dataset.xlsx")
test = test.to_json(orient='records') #reorientates
test = json.loads(test)
response = r.post(base_url +'predict', json = test)

#Test repsonse

if response.status_code == 200:
    print('Request Successful.')
    print('...')
    print('Location Accuracy Predictions Ready.')

else:
    print('Request Failed.')