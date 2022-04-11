from django import forms
import requests
import json
import pandas as pd
import numpy as np


url = 'http://requisite.ad.rfa.space/nc/gnc_test_database_dzpx/api/v1/Requirements'
#payload = open("request.json")
headers = {'xc-auth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJ1ZHJhd3JpdC5tYWp1bWRhckByZmEuc3BhY2UiLCJmaXJzdG5hbWUiOm51bGwsImxhc3RuYW1lIjpudWxsLCJpZCI6Nywicm9sZXMiOiJ1c2VyIiwiaWF0IjoxNjQ4ODM3MTI1fQ.gC7bcZVMTvwpKTU8nlZrxmfKrapUXhTtrwlVS9EzNi4'}
r = requests.get(url, headers=headers)

dict = json.loads(r.text)
df = pd.json_normalize(dict)

df.reset_index(drop =True, inplace =True)
print(df.head())
df = df.drop(['Id', 'CreatedAt', 'UpdatedAt', 'requirements_id'], axis =1)
columns = list(df.columns)

tup_columns =list(zip(columns, columns))
tup_columns = tuple(tup_columns)
print(tup_columns)
OPTIONS = tup_columns
        
class WikiForm(forms.Form):
    
    filters = forms.MultipleChoiceField( choices=OPTIONS, label= '')